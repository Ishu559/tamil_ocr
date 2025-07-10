from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

# Assuming your OCR logic is in a file like 'ocr_processor.py'
# And it has a function like 'process_image_for_ocr'
# You might need to adjust paths or structure based on your actual project.
try:
    from ocr_processor import process_image_for_ocr
except ImportError:
    # Placeholder for your actual OCR logic
    def process_image_for_ocr(image_path: str):
        # In a real scenario, this would call your OCR functions
        print(f"Processing OCR for: {image_path}")
        return {"text": "Detected text from image", "language": "Tamil"}

app = FastAPI(
    title="Tamil OCR API",
    description="A REST API for performing Optical Character Recognition on Tamil text.",
    version="1.0.0",
)

class OCRResult(BaseModel):
    text: str
    language: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Tamil OCR API! Go to /docs for API documentation."}

@app.post("/ocr/", response_model=OCRResult)
async def perform_ocr_on_image(file: UploadFile = File(...)):
    """
    Performs OCR on an uploaded image file.
    """
    upload_folder = "uploaded_images"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call your actual OCR processing function here
    ocr_output = process_image_for_ocr(file_path)

    # Clean up the uploaded file
    os.remove(file_path)

    return ocr_output

# You can add more endpoints, e.g., for OCR from a URL or specific options
