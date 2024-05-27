import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY: str = os.getenv('SECRET_KEY')
ALGORITHM: str = os.getenv('ALGORITHM')
OPEN_API_BASE: str = os.getenv('OPEN_API_BASE')
