FROM public.ecr.aws/lambda/python:3.9
COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY main.py ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt
CMD [ "main.handler" ]