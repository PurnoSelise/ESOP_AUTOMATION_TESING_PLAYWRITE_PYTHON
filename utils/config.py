import yaml, os
from dotenv import load_dotenv

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def get_credentials():
    load_dotenv()
    return {
        "username": os.getenv("LOGIN_USER"),
        "password": os.getenv("LOGIN_PASS"),
        "webpass": os.getenv("WEBSHOP_PASS")
    }
