import boto3
import os
import xmltodict


MTURK_ENDPOINT_URL = 'https://mturk-requester.us-east-1.amazonaws.com'
MTURK_SANDBOX_ENDPOINT_URL = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

mturk = boto3.client(
   'mturk',
   aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
   aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
   region_name='us-east-1',
   endpoint_url=MTURK_SANDBOX_ENDPOINT_URL
)
hit_id = '3XAOZ9UYRZRNQ54YRMWMMB421XS1QB'# full test run '3BJKPTD2QCCOBQV76K5WX7X2PPRRTR'
worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Approved', 'Submitted'])

if worker_results['NumResults'] > 0:
    for assignment in worker_results['Assignments']:
        xml_doc = xmltodict.parse(assignment['Answer'])
        print("Worker's answer was:")
        if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
            # Multiple fields in HIT layout
            for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
                print("For input field: " + answer_field['QuestionIdentifier'])
                print("Submitted answer: " + answer_field['FreeText'] if answer_field['FreeText'] else "")
        else:
            # One field found in HIT layout
            print("For input field: " + xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
            print("Submitted answer: " + xml_doc['QuestionFormAnswers']['Answer']['FreeText'])
else:
    print("No results ready yet")
