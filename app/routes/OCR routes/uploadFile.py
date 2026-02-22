from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import pytesseract
import io


router = APIRouter(prefix="/ocr", tags=['Upload Image'])

@router.post("/uploadFile")
async def characterRecognition(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        extracted_text = pytesseract.image_to_string(image)
        return {
            "filename": file.filename,
            "extracted_text": extracted_text
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Image is not readable")
