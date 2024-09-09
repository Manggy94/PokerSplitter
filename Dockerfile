ARG PYTHON_VERSION=3.12
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

ARG PACKAGE_NAME=pkrsplitter
ARG HANDLER="pkrsplitter.lambda.history_splitter.lambda_handler"
ARG USELESS_DIRS
ARG USELESS_FILES

COPY ${PACKAGE_NAME}/ ${LAMBDA_TASK_ROOT}/$PACKAGE_NAME/
COPY config/lambda_entrypoint.sh ${LAMBDA_TASK_ROOT}/lambda_entrypoint.sh
COPY ${USELESS_DIRS} ${LAMBDA_TASK_ROOT}/useless_dirs.txt
COPY ${USELESS_FILES} ${LAMBDA_TASK_ROOT}/useless_files.txt

RUN cat ${LAMBDA_TASK_ROOT}/useless_dirs.txt
RUN cat ${LAMBDA_TASK_ROOT}/useless_files.txt
# RUN cat ${LAMBDA_TASK_ROOT}/useless_dirs.txt | xargs rm -rf
# RUN cat ${LAMBDA_TASK_ROOT}/useless_files.txt | xargs rm

RUN rm -rf ${LAMBDA_TASK_ROOT}/pkrsplitter/runs
RUN  rm ${LAMBDA_TASK_ROOT}/pkrsplitter/settings.py ${LAMBDA_TASK_ROOT}/pkrsplitter/splitters/local.py

COPY config/app_requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Specify entrypoint for lambda
CMD [${HANDLER}]
