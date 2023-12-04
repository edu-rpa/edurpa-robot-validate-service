import base64
import boto3
import json
import os
import datetime

ecs_client = boto3.client('ecs')

def lambda_handler(event, context):
    # Get ECS cluster, task definition, and container name
    ecs_cluster = 'robot'

    if event["body"]:
        body=json.loads(event["body"])
    else:
        body=event
    taskID = body['taskID']

    response = ecs_client.stop_task(
        cluster=ecs_cluster,
        task = taskID,
    )

    return {
        "statusCode": 200,
        "headers": { 'Content-Type': 'text/json' },
        "body": json.dumps(response, indent=4, sort_keys=True, default=str)
    }
