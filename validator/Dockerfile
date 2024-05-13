FROM public.ecr.aws/lambda/python:3.9

RUN yum install -y mesa-libGL.x86_64

COPY requirements.txt ./

RUN python3.9 -m pip install -r requirements.txt

# install the cv2 dependencies that are normally present on the local machine, 
# but might be missing in your Docker container causing the issue.

RUN python3.9 -m pip install edurpa-cloud

RUN python3.9 -m pip install edurpa-document

RUN pip install torch torchvision -f https://download.pytorch.org/whl/cpu/torch_stable.html

COPY app.py upload_run.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
