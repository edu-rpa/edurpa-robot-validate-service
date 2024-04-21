from robot.api import TestSuite
from robot import run
from upload_run import parse_robot_result
import xml.etree.ElementTree as ET
import json
import os

def lambda_handler(event, context):
    print(event)
    
    if event["body"]:
        data=json.loads(event["body"])
    else:
        data=event
    # Dry run test from dict
    robot = TestSuite(rpa=True).from_dict(data)
    outputdir = f'/tmp/validator/{context.aws_request_id}/'
    try:
        robot.run(outputdir = outputdir, dryrun=True)
    except Exception as e:
        print(e)
    xml_file_path = f'{outputdir}output.xml'
    
    os.environ["UUID_STREAM"] = ""
    res = parse_robot_result(xml_file_path,'','')

    response = {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": json.dumps(res),
    }

    return response
