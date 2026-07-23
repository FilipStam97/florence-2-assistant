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

from util import Prompt, annotate_ocr

BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

app = FastAPI(title="Florence2 Demo")
model = Florence2Model()

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
    if image.filename is None:
        raise ValueError("Image has no filename")

    preparedRes = get_res_by_prompt(prompt, image, text_input)
    return preparedRes



def parse_florence_res(res):
     return next(iter(res.values()))


def  get_res_by_prompt(prompt: str, image: UploadFile, text_input = None):    
      filename = image.filename or "image.jpg"
      extension = Path(filename).suffix or ".jpg"
      pil_image = Image.open(image.file).convert("RGB")
      res = model.run(image=pil_image, task_prompt=prompt, text_input=text_input)
      print("Raw Florence 2 response ->",res)

      caption_prompts = {
            Prompt.CAPTION.value,
            Prompt.DETAILED_CAPTION.value,
            Prompt.MORE_DETAILED_CAPTION.value,
            Prompt.OCR.value,
            Prompt.REGION_TO_CATEGORY.value,
            Prompt.REGION_TO_DESCRIPTION.value,
            Prompt.REGION_TO_OCR.value
        }

      annotation_prompts = {
            Prompt.OCR_WITH_REGION.value,
            Prompt.OD.value,
            Prompt.DENSE_REGION_CAPTION.value,
            Prompt.REGION_PROPOSAL.value,
            Prompt.CAPTION_TO_PHRASE_GROUNDING.value
        }

      parsedRes = parse_florence_res(res)
      
      match prompt:
           case p if p in caption_prompts:
                return {"caption": parsedRes}
           case p if p in annotation_prompts:
                upload_path = UPLOADS_DIR / f"{uuid.uuid4().hex}{extension}"
                pil_image.save(upload_path)
                out_filename = annotate_ocr(parsedRes, upload_path)
                if out_filename is None:
                        raise ValueError("Image has no filename")
                return {"imgSrc": f"/outputs/{out_filename}"}
           case _:
                return res