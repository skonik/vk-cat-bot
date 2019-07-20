import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('.').parent / '.env'
load_dotenv(dotenv_path=env_path)

VK_ACCESS_TOKEN = os.environ['VK_ACCESS_TOKEN']
VK_CONFIRMATION_CODE = os.environ['VK_CONFIRMATION_CODE']
GIPHY_ACCESS_TOKEN = os.environ['GIPHY_ACCESS_TOKEN']
