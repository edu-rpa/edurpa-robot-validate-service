# CMD
source build_script.sh
sam deploy (--guided for first time) 

upload_run.py: parse result librabry pull using included in build_script.sh
``` bash
aws s3 cp s3://edu-rpa-robot/utils/upload_run.py ./validator
```

The lib is written in [text](https://github.com/edu-rpa/edu-rpa-serverless-robot)

