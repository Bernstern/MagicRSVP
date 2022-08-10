FROM public.ecr.aws/lambda/python:3.6

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN --mount=type=cache,target=/root/.cache/pip python3.6 -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip python3.6 -m pip install -r requirements.txt

COPY web.py ${LAMBDA_TASK_ROOT}

CMD [ "web.handler" ]