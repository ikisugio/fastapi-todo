import os
from dotenv import load_dotenv
from settings import (
    ec2_entry_script_path,
    env_file_path,
    ingress_args,
)


with open(ec2_entry_script_path, 'r') as file:
    ec2_entry_script = file.read()

load_dotenv(env_file_path)
aws_envs = {key.lower(): val for key, val in os.environ.items()}

ingress_dicts = [
    {k: aws_envs[k] for k in ingress_args},
                 ]