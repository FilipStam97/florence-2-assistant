import requests
from PIL import Image
import os
import shutil
from uuid import uuid4
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from predictor  import Florence2Model   
from typing import Optional
from pathlib import Path
import uuid
import json

from util import annotate_ocr

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

app = FastAPI(title="GroundingDINO Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")

@app.get("/health")
def health():
    return {"status": "ok"}



@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    text_input: Optional[str] = Form(None)
):
    
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")
    
    model = Florence2Model()
    pil_image = Image.open(image.file).convert("RGB")

    res = model.run(image=pil_image, task_prompt=prompt, text_input=text_input)

    if(prompt == "<OCR_WITH_REGION>"):
        if image.filename is None:
            raise ValueError("Image has no filename")
        filename = image.filename or "image.jpg"
        extension = Path(filename).suffix or ".jpg"
        upload_path = UPLOADS_DIR / f"{uuid.uuid4().hex}{extension}"
        pil_image.save(upload_path)

        first_value = next(iter(res.values()))
        print(first_value)

        out_filename = annotate_ocr(first_value, upload_path)

        if out_filename is None:
                raise ValueError("Image has no filename")
        
        return {"imgSrc": f"/outputs/{out_filename}"}
     

    print(res)
    return res