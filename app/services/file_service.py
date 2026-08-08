import os
import uuid
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def save_file(file: UploadFile, folder: str):
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400,
                            detail="Only JPG, JPEG and PNG files are allowed.")
    contents = file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400,
                            detail="Maximum file size is 5 MB.")
    filename = f"{uuid.uuid4()}{extension}"
    filepath = os.path.join(folder, filename)
    with open(filepath, "wb") as f:
        f.write(contents)
    return filename