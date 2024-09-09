ARG PYTHON_VERSION
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

ARG PACKAGE_NAME
ARG HANDLER
ARG USELESS_DIRS
ARG USELESS_FILES

COPY ${PACKAGE_NAME}/ ${LAMBDA_TASK_ROOT}/$PACKAGE_NAME/
COPY ${USELESS_DIRS} ${LAMBDA_TASK_ROOT}/useless_dirs.txt
COPY ${USELESS_FILES} ${LAMBDA_TASK_ROOT}/useless_files.txt
COPY config/app_requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt

WORKDIR ${LAMBDA_TASK_ROOT}

RUN for dir in $(cat useless_dirs.txt | tr -d '\r'); do rm -rf ${dir}; done
RUN for file in $(cat useless_files.txt | tr -d '\r'); do rm ${file}; done
RUN pip install -r requirements.txt

CMD [ $HANDLER ]
