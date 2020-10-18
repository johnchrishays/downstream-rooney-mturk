from django.core.management.base import BaseCommand, CommandError
from experiment.models import SelectionProcess, ResultHIT
import xmltodict
import pandas as pd
import boto3
import os

n_iterations = 3

class Command(BaseCommand):
    help  = "Queries the database"

    def add_arguments(self, parser):
        parser.add_argument('host', type=str, metavar="host")

    def handle(self, *args, **options):
        if (options['host'] == 'heroku'):
            self.__handle_local()
        else:
            self.__handle_mturk()

    def __assn_to_df(self, assignment):
        xml_doc = xmltodict.parse(assignment['Answer'])
        new_dict = dict()
        if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
            # Multiple fields in HIT layout
            for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
                if (answer_field['QuestionIdentifier'] in {"true_utility[]","perc_utility[]","num_selected_x_cands[]"}):
                    new_dict[answer_field['QuestionIdentifier']] = list(map(float, answer_field['FreeText'].split("|")))
                else:
                    new_dict[answer_field['QuestionIdentifier']] = [answer_field['FreeText'] for i in range(n_iterations)]
        else:
            # One field found in HIT layout
            new_dict[xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier']] = list(map(float, xml_doc['QuestionFormAnswers']['Answer']['FreeText']))
        return pd.DataFrame(new_dict)

    def __handle_mturk(self):
        MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

        mturk = boto3.client(
            'mturk',
            aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name='us-east-1',
            endpoint_url = MTURK_SANDBOX
        )
        hit_id = '3MD8CKRQZZNUXNZ2UQRSV1ATQ7XRJM'
        worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Approved', 'Submitted'])
        df = pd.DataFrame()
        self.stdout.write("Querying MTurk database.")
        if worker_results['NumResults'] > 0: 
            assn_dfs = [self.__assn_to_df(assignment) for assignment in worker_results['Assignments']]
            df = pd.concat(assn_dfs)
            df.to_pickle("results_mturk.pkl")
        else:
           print("No results ready yet")
        
    def __handle_local(self):
        self.stdout.write("Querying heroku database.")
        # ResultHIT.objects.all().delete()
        concat_lst = [pd.DataFrame(obj.to_dict()) for obj in ResultHIT.objects.all()]
        if (len(concat_lst) > 0):
            df = pd.concat(concat_lst)
            df.to_pickle("results_heroku.pkl")
        else:
            print("No objects in DB!")
