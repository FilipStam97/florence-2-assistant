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

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOADS_DIR = os.path.join(PROJECT_ROOT, "uploads")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")

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
    model = Florence2Model()
    pil_image = Image.open(image.file).convert("RGB")


    res = model.run(image=pil_image, task_prompt=prompt, text_input=text_input)
    print(res)
    return res