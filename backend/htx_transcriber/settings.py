import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

ENV = os.getenv("ENV")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

UPLOAD_DIR = os.getenv("UPLOAD_DIR")
if not UPLOAD_DIR:
    raise ValueError("UPLOAD_DIR is not set")
Path(UPLOAD_DIR).mkdir(exist_ok=True)
