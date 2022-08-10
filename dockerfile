FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN --mount=type=cache,target=/root/.cache/pip python3.8 -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip python3.8 -m pip install -r requirements.txt

COPY app.py ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]