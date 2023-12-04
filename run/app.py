import base64
import boto3
import json
import os
import datetime

ecs_client = boto3.client('ecs')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get ECS cluster, task definition, and container name
    ecs_cluster = 'robot'
    ecs_task_definition = 'grade-robot'
    ecs_container_name = 'grading'
    ecs_image = '437372835847.dkr.ecr.ap-southeast-1.amazonaws.com/grading-robot'

    if event["body"]:
        body=json.loads(event["body"])
    else:
        body=event

    name = body['name']
    robotJSON = body['data']
    current = datetime.datetime.now().strftime("%Y%m%d%H%M%SZ")
    # file_content = json.dumps(data)

    # # Create a temporary file in /tmp with the content
    # temp_file_path = '/tmp/robot.json'
    # with open(temp_file_path, 'w') as temp_file:
    #     temp_file.write(file_content)

    updated_file_content = robotJSON
    s3_bucket = 'daivdtech.click'
    s3_key = f'{name}/robot_{current}.json'

    # Upload the updated file to S3
    s3_client.put_object(Body=json.dumps(updated_file_content).encode('utf-8'), Bucket=s3_bucket, Key=s3_key)

    # Get the ECS task ARN
    response = ecs_client.run_task(
        cluster=ecs_cluster,
        taskDefinition=ecs_task_definition,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['subnet-0b151e98751281583', 'subnet-0e6e072787344aa5c', 'subnet-0df0a392aead18a0c'],
                'securityGroups': ['sg-0ee6088d9de8910e6'],
                'assignPublicIp': 'ENABLED'
            }
        },
    )

    #     overrides={
    #     'containerOverrides': [
    #         {
    #             'name': ecs_container_name,
    #             'command': [f'/bin/sh', '-c', f'aws s3 cp s3://{s3_bucket}/{s3_key} /ecs-mount-path/app/robot.json']
    #         }
    #     ]
    # }

    return {
        "statusCode": 200,
        "headers": { 'Content-Type': 'text/json' },
        "body": json.dumps(response, indent=4, sort_keys=True, default=str)
    }
