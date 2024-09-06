ARG PYTHON_VERSION=3.12
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

ARG PACKAGE_NAME=pkrsplitter
RUN echo ${PACKAGE_NAME}
RUN echo ${PYTHON_VERSION}

COPY ${PACKAGE_NAME}/ ${LAMBDA_TASK_ROOT}/$PACKAGE_NAME/

RUN rm -rf ${LAMBDA_TASK_ROOT}/pkrsplitter/runs
RUN  rm ${LAMBDA_TASK_ROOT}/pkrsplitter/settings.py ${LAMBDA_TASK_ROOT}/pkrsplitter/splitters/local.py

COPY config/app_requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Spécifier le point d'entrée pour Lambda
CMD ["pkrsplitter.lambda.history_splitter.lambda_handler"]
