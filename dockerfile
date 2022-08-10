FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN --mount=type=cache,target=/root/.cache/pip python3.8 -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip python3.8 -m pip install -r requirements.txt

COPY app.py ${LAMBDA_TASK_ROOT}

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
ENV AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}

CMD [ "app.handler" ]