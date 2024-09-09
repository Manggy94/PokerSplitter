ARG PYTHON_VERSION
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

ARG PACKAGE_NAME
ARG HANDLER
ARG USELESS_DIRS
ARG USELESS_FILES

COPY ${PACKAGE_NAME}/ ${LAMBDA_TASK_ROOT}/$PACKAGE_NAME/
COPY ${USELESS_DIRS} ${LAMBDA_TASK_ROOT}/useless_dirs.txt
COPY ${USELESS_FILES} ${LAMBDA_TASK_ROOT}/useless_files.txt

WORKDIR ${LAMBDA_TASK_ROOT}
RUN echo $(cat useless_dirs.txt)
RUN echo $(cat useless_files.txt)
RUN cat useless_dirs.txt | xargs rm -rf
RUN cat useless_files.txt | xargs rm

WORKDIR ..

RUN rm -rf ${LAMBDA_TASK_ROOT}/pkrsplitter/runs
RUN  rm ${LAMBDA_TASK_ROOT}/pkrsplitter/settings.py ${LAMBDA_TASK_ROOT}/pkrsplitter/splitters/local.py

COPY config/app_requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

CMD [${HANDLER}]
