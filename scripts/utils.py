import boto3
import os
import zipfile


def create_zip_archive(source_dir: str, dist_dir: str, archive_name: str, archive_path: str, package_name: str):
    """
    Creates a zip archive of the package with the package name as the root directory
    """
    print(f"Zipping {source_dir} to {dist_dir} as {archive_name}")
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    with zipfile.ZipFile(archive_path, "w") as z:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".py"):
                    source_path = os.path.join(root, file)
                    relative_path = os.path.relpath(source_path, source_dir)
                    dest_path = os.path.join(package_name, relative_path)
                    z.write(source_path, dest_path)
    print(f"Created {archive_name}")


def create_zip_layer(dist_dir: str):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    layer_dir = os.path.join(base_dir, "tmp/layer")
    layer_path = os.path.join(dist_dir, "layer.zip")
    with zipfile.ZipFile(layer_path, "w") as z:
        for root, dirs, files in os.walk(layer_dir):
            for file in files[:3]:
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, layer_dir)
                z.write(source_path, relative_path)
    print("Created layer.zip")


def publish_layer(package_name: str):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    layer_path = os.path.join(base_dir, "dist/layer.zip")
    lambda_client = boto3.client('lambda', region_name='eu-west-3')
    layer_name = f"{package_name}_layer"
    with open(layer_path, 'rb') as f:
        zip_content = f.read()
    lambda_client.publish_layer_version(
        LayerName=layer_name,
        Description=f"{package_name} layer",
        Content={'ZipFile': zip_content}
    )


def connect_lambda_to_layer(function_name: str, layer_name: str):
    """
    Connects a lambda function to a layer
    """
    print(f"Connecting lambda function {function_name} to layer {layer_name}")
    lambda_client = boto3.client('lambda')
    layer_arn = lambda_client.list_layer_versions(LayerName=layer_name)['LayerVersions'][0]['LayerVersionArn']
    lambda_client.update_function_configuration(
        FunctionName=function_name,
        Layers=[layer_arn],
    )
    print(f"Connected lambda function {function_name} to layer {layer_name}")


def get_lambda_role(function_role: str):
    """
    Returns the ARN of the lambda role
    """
    iam = boto3.client('iam')
    role = iam.get_role(RoleName=function_role)
    return role['Role']['Arn']


def display_function_info(function_name: str, lambda_client):
    """
    Displays the information of a lambda function
    """
    print(f"Getting function information for {function_name}")
    fct = lambda_client.get_function(FunctionName=function_name)
    print(f"Function information for {function_name}: {fct}")


def display_function_config(function_name: str, lambda_client):
    """
    Displays the configuration of a lambda function
    """
    print(f"Getting function configuration for {function_name}")
    conf = lambda_client.get_function_configuration(FunctionName=function_name)
    print(f"Function configuration for {function_name}: {conf}")


def update_function_config(lambda_client, function_name: str, runtime: str, lambda_handler: str, function_role: str):
    """
    Updates the configuration of a lambda function
    """
    print(f"Updating function configuration for {function_name}")
    role_arn = get_lambda_role(function_role=function_role)
    lambda_client.update_function_configuration(
        FunctionName=function_name,
        Handler=lambda_handler,
        Runtime=runtime,
        Role=role_arn,
    )
    # Wait for the configuration update to complete
    lambda_client.get_waiter('function_updated').wait(FunctionName=function_name)
    print(f"Update for {function_name} configuration complete")
    # Displays updated function configuration
    print(f"Updated function configuration for {function_name}")


def update_function_code(lambda_client, function_name: str, archive_path: str):
    """
    Updates the code of a lambda function
    """
    print(f"Updating function code for {function_name}")
    with open(archive_path, 'rb') as f:
        zipped_code = f.read()
    lambda_client.update_function_code(
        FunctionName=function_name,
        ZipFile=zipped_code,
    )
    # Wait for the code update to complete
    lambda_client.get_waiter('function_updated').wait(FunctionName=function_name)
    print(f"Update for {function_name} code complete")
    # Displays updated function information
    print(f"Updated function code for {function_name}")


def update_function(lambda_client, function_name: str, runtime: str, lambda_handler: str, function_role: str,
                    archive_path: str):
    """
    Updates a lambda function
    """
    update_function_config(lambda_client=lambda_client, function_name=function_name, runtime=runtime,
                           lambda_handler=lambda_handler, function_role=function_role)
    update_function_code(lambda_client=lambda_client, function_name=function_name, archive_path=archive_path)
    print(f"Updated lambda function {function_name}")


def create_function(lambda_client, function_name: str, archive_path: str, runtime: str, lambda_handler: str,
                    function_role: str):
    """
    Creates a lambda function
    """
    print(f"Creating lambda function {function_name}")
    with open(archive_path, 'rb') as f:
        zipped_code = f.read()
    role_arn = get_lambda_role(function_role=function_role)
    lambda_client.create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role_arn,
        Handler=lambda_handler,
        Code=dict(ZipFile=zipped_code),
    )
    print(f"Created lambda function {function_name}")


def make_lambda_function(function_name: str, archive_path: str, runtime: str, lambda_handler: str, function_role: str):
    """
    Creates a lambda function
    """
    lambda_client = boto3.client('lambda')
    try:
        create_function(lambda_client=lambda_client, function_name=function_name, archive_path=archive_path,
                        runtime=runtime, lambda_handler=lambda_handler, function_role=function_role)
    except lambda_client.exceptions.ResourceConflictException:
        print(f"Function {function_name} already exists")
        display_function_info(function_name=function_name, lambda_client=lambda_client)
        display_function_config(function_name=function_name, lambda_client=lambda_client)
        update_function(lambda_client=lambda_client, function_name=function_name, runtime=runtime,
                        lambda_handler=lambda_handler, function_role=function_role, archive_path=archive_path)


def get_roles():
    iam = boto3.client('iam')
    roles = iam.list_roles()
    for role in roles['Roles']:
        print(role['RoleName'])


def get_bucket_info():
    s3 = boto3.client('s3')
    bucket_name = "pokerbrain"
    json_info = s3.get_bucket_policy(Bucket=bucket_name)
    print(json_info)
