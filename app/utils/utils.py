import hashlib
import os.path
import shutil
from pathlib import Path

from fastapi import UploadFile, HTTPException
from fastapi.templating import Jinja2Templates

def get_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_image(manufacturer_name, file:UploadFile):
    filename = f'{manufacturer_name}{Path(file.filename).suffix}'
    try:
        with open(f"../static/img/manufacturers_images/{filename}", 'wb+') as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    return filename

templates = Jinja2Templates(directory="../templates")
