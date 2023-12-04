FROM public.ecr.aws/lambda/python:3.9

# Install git
RUN yum install -y git

RUN git clone https://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@github.com/edu-rpa/edu-rpa-library.git

COPY requirements.txt ./

RUN python3.9 -m pip install -r requirements.txt -t .

COPY app.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
