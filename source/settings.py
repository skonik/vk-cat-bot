import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

VK_ACCESS_TOKEN = os.environ['VK_ACCESS_TOKEN']
VK_CONFIRMATION_CODE = os.environ['VK_CONFIRMATION_CODE']
GIPHY_ACCESS_TOKEN = os.environ['GIPHY_ACCESS_TOKEN']
