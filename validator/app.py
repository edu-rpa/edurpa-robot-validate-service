from robot.api import TestSuite
from robot import run
from upload_run import parse_robot_result
import xml.etree.ElementTree as ET
import json
import os

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
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
    parse_robot_result(xml_file_path,'','')

    response = {
        "statusCode": 200,
        "result": parse_robot_result(xml_file_path,'',''),
    }

    return response
