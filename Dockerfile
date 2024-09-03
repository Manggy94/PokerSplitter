# Utiliser l'image de base AWS Lambda pour Python 3.10
FROM public.ecr.aws/lambda/python:3.10

# Copier le code de la fonction
COPY pkrsplitter/ ${LAMBDA_TASK_ROOT}/pkrsplitter/

# Installer les paquets requis
COPY config/app_requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Spécifier le point d'entrée pour Lambda
CMD ["pkrsplitter.lambda.history_splitter.lambda_handler"]
