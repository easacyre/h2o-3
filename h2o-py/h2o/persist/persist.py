import h2o
from h2o.exceptions import H2OValueError


def set_s3_credentials(secret_key_id, secret_access_key):
    """Creates a new Amazon S3 client internally with specified credentials.
    There are no validations done to the credentials. Incorrect credentials are thus revealed with first S3 import call.
    
    secretKeyId Amazon S3 Secret Key ID (provided by Amazon)
    secretAccessKey Amazon S3 Secret Access Key (provided by Amazon)
    """
    if(secret_key_id is None):
        raise H2OValueError("Secret key ID must be specified")

    if(secret_access_key is None):
        raise H2OValueError("Secret access key must be specified")
    
    if(not secret_key_id):
        raise H2OValueError("Secret key ID must not be empty")
    
    if(not secret_access_key):
        raise H2OValueError("Secret access key must not be empty")
    
    
    params = {"secret_key_id": secret_key_id,
              "secret_access_key": secret_access_key
              }
    
    h2o.api(endpoint="POST /3/PersistS3", data=params)
    print("Credentials successfully set.")

def set_s3a_credentials(access_key_id, secret_access_key):
    """Sets AWS credentials for Hadoop S3A dynamically
    Providing incorrect credentials results in an error during the first related S3A import call.
    
    access_key_id S3 Secret Key ID (provided by Amazon, corresponds to fs.s3.awsAccessKeyId)
    secret_access_key Amazon S3 Secret Access Key (provided by Amazon, corresponds to fs.s3.awsSecretAccessKey)
    """
    if(access_key_id is None):
        raise H2OValueError("Secret key ID must be specified")

    if(secret_access_key is None):
        raise H2OValueError("Secret access key must be specified")

    if(not access_key_id):
        raise H2OValueError("Secret key ID must not be empty")

    if(not secret_access_key):
        raise H2OValueError("Secret access key must not be empty")


    params = {"access_key_id": access_key_id,
              "secret_access_key": secret_access_key
              }

    h2o.api(endpoint="POST /3/PersistS3A", data=params)
    print("Credentials successfully set.")
