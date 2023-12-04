import base64
import boto3
import json
import os

ecs_client = boto3.client('ecs')
def lambda_handler(event, context):
    # Get ECS cluster, task definition, and container name
    ecs_cluster = 'robot'
    ecs_task_definition = 'grade-robot'
    ecs_container_name = 'robot-david'
    ecs_image = '437372835847.dkr.ecr.ap-southeast-1.amazonaws.com/grading-robot'

    if event["body"]:
        data=json.loads(event["body"])
    else:
        data=event

    file_content = json.dumps(data)

    # Create a temporary file in /tmp with the content
    temp_file_path = '/tmp/robot.json'
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(file_content)

    # Get the ECS task ARN
    response = ecs_client.run_task(
        cluster=ecs_cluster,
        taskDefinition=ecs_task_definition,
        launchType='FARGATE',
        overrides={
            'containerOverrides': [
                {
                    'name': ecs_container_name,
                    "image": ecs_image,
                    'command': [f'/bin/sh', '-c', 'cat {temp_file_path} > /ecs-mount-path/app/{temp_file_path}']
                }
            ]
        }
    )

    # Clean up the temporary file
    os.remove(temp_file_path)

    return response
