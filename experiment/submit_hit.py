import boto3
import os
import sys
import psycopg2

USING_SANDBOX = False

new_hit_params = [
    {
        "n_x": 50,
        "n_y": 50,
        "k": 10,
        "l": 0,
        "bias": 2/3,
        "n_iterations": 24,
        "pts_per_dollar": 15000,
        "base_reward": f"{1.00:0.2f}",
        "avg_bonus_reward": f"{1.20:0.2f}",
        "avg_n_minutes_to_complete": 20,
        "using_sandbox": True,
    } for _ in range(3)] + \
    [{
        "n_x": 50,
        "n_y": 50,
        "k": 10,
        "l": 1,
        "bias": 2/3,
        "n_iterations": 24,
        "pts_per_dollar": 15000,
        "base_reward": f"{1.00:0.2f}",
        "avg_bonus_reward": f"{1.20:0.2f}",
        "avg_n_minutes_to_complete": 20,
        "using_sandbox": True,
    } for _ in range(3)] + \
    [{
        "n_x": 50,
        "n_y": 50,
        "k": 10,
        "l": 2,
        "bias": 2/3,
        "n_iterations": 24,
        "pts_per_dollar": 15000,
        "base_reward": f"{1.00:0.2f}",
        "avg_bonus_reward": f"{1.20:0.2f}",
        "avg_n_minutes_to_complete": 20,
        "using_sandbox": True,
    } for _ in range(3)] + \
    [{
        "n_x": 50,
        "n_y": 50,
        "k": 10,
        "l": 0,
        "bias": 0.9,
        "n_iterations": 24,
        "pts_per_dollar": 15000,
        "base_reward": f"{1.00:0.2f}",
        "avg_bonus_reward": f"{1.20:0.2f}",
        "avg_n_minutes_to_complete": 20,
        "using_sandbox": True,
    } for _ in range(3)] + \
    [{
        "n_x": 50,
        "n_y": 50,
        "k": 10,
        "l": 1,
        "bias": 0.9,
        "n_iterations": 24,
        "pts_per_dollar": 15000,
        "base_reward": f"{1.00:0.2f}",
        "avg_bonus_reward": f"{1.20:0.2f}",
        "avg_n_minutes_to_complete": 20,
        "using_sandbox": True,
    } for _ in range(3)] + \
    [{
        "n_x": 50,
        "n_y": 50,
        "k": 10,
        "l": 2,
        "bias": 0.9,
        "n_iterations": 24,
        "pts_per_dollar": 15000,
        "base_reward": f"{1.00:0.2f}",
        "avg_bonus_reward": f"{1.20:0.2f}",
        "avg_n_minutes_to_complete": 20,
        "using_sandbox": True,
    } for _ in range(3)]

if __name__ == "__main__":
    MTURK_ENDPOINT_URL = 'https://mturk-requester.us-east-1.amazonaws.com'
    MTURK_SANDBOX_ENDPOINT_URL = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    mturk = boto3.client('mturk',
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                         region_name='us-east-1',
                         endpoint_url=MTURK_SANDBOX_ENDPOINT_URL if USING_SANDBOX else MTURK_ENDPOINT_URL
                         )
    print(f"There is ${mturk.get_account_balance()['AvailableBalance']} in the account.")

    if (len(sys.argv) <= 1):
        connection = psycopg2.connect(os.environ['DATABASE_URL'])
        cursor = connection.cursor()
        for param_dict in new_hit_params:
            cursor.execute(
                f"INSERT INTO experiment_queuedhitparams (n_x,n_y,k,l,bias,n_iterations,pts_per_dollar,base_reward,avg_bonus_reward,avg_n_minutes_to_complete,using_sandbox) VALUES ("
                f"{param_dict['n_x']},"
                f"{param_dict['n_y']},"
                f"{param_dict['k']},"
                f"{param_dict['l']},"
                f"{param_dict['bias']},"
                f"{param_dict['n_iterations']},"
                f"{param_dict['pts_per_dollar']},"
                f"{param_dict['base_reward']},"
                f"{param_dict['avg_bonus_reward']},"
                f"{param_dict['avg_n_minutes_to_complete']},"
                f"{param_dict['using_sandbox']}"
                ");"
                )

        # cursor.execute("SELECT * FROM experiment_queuedhitparams ORDER BY random() LIMIT 1;")
        # for row in cursor.fetchall():
        #     print(row)

        # cursor.execute("SELECT * FROM experiment_queuedhitparams")
        # for row in cursor.fetchall():
        #     print(row)

        connection.commit()
        connection.close()
        # # Submit HIT to MTurk
        question = open(file=os.path.join(sys.path[0],'questions.xml'), mode='r').read()
        new_hit = mturk.create_hit(
            Title='Academic study (~10 min, ~$1.20 bonus)',
            Description='Over several iterations, try to collect the greatest reward',
            Keywords='',
            Reward='1.00',
            MaxAssignments=9,
            LifetimeInSeconds=86400,
            AssignmentDurationInSeconds=900,
            AutoApprovalDelayInSeconds=86400,
            Question=question,
            QualificationRequirements=[
                {
                    'QualificationTypeId': "00000000000000000071",
                    'Comparator': 'EqualTo',
                    'LocaleValues':[{ 'Country':'US' }],
                    'ActionsGuarded':'DiscoverPreviewAndAccept'
                },
            ],
        )
    else:
        worker_id = sys.argv[1]
        reward = sys.argv[2]
        question = open(file=os.path.join(sys.path[0],'pay_bonus.xml'), mode='r').read()
        response = mturk.create_qualification_type(
            Name=worker_id,
            Keywords=worker_id,
            Description=f'Qualification ONLY for {worker_id}',
            QualificationTypeStatus='Active',
            RetryDelayInSeconds=123,
            TestDurationInSeconds=123,
            AutoGranted=False,
        )
        qual_id = response['QualificationType']['QualificationTypeId']
        response = mturk.associate_qualification_with_worker(
            QualificationTypeId=qual_id,
            WorkerId=worker_id,
            IntegerValue=23,
            SendNotification=True
        )
        new_hit = mturk.create_hit(
            Title=f'This HIT is for {worker_id} only —— all others will be rejected',
            Description=f'Confirm you are the worker for this hit',
            Keywords=f'{worker_id}',
            Reward=f'{reward}',
            MaxAssignments=1,
            LifetimeInSeconds=86400,
            AssignmentDurationInSeconds=1800,
            AutoApprovalDelayInSeconds=86400,
            Question=question,
            QualificationRequirements=[
                {
                    'QualificationTypeId': qual_id,
                    'Comparator': 'EqualTo',
                    'IntegerValues': [
                        23,
                    ],
                    'ActionsGuarded':'DiscoverPreviewAndAccept'
                },
            ],
        )
    print("A new HIT has been created:")
    if (USING_SANDBOX):
        print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
    else:
        print("https://worker.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
    print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
