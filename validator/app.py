from robot.api import TestSuite
import xml.etree.ElementTree as ET
import json

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
    robot = TestSuite().from_dict(data)
    outputdir = f'/tmp/validator/{context.aws_request_id}/'
    try:
        robot.run(outputdir = outputdir, dryrun = True)
    except:
        pass
    xml_file_path = f'{outputdir}output.xml'

    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    xml_string = ET.tostring(root, encoding='unicode')
    print(xml_string)
    response = {
        "statusCode": 200,
        "headers": { 'Content-Type': 'text/xml' },
        "body": xml_string
    }

    return response
