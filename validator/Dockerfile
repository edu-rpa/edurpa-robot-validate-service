FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ./

RUN python3.9 -m pip install -r requirements.txt

RUN python3.9 -m pip install edurpa-cloud

RUN python3.9 -m pip install edurpa-document

COPY app.py upload_run.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
