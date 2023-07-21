from fastapi import APIRouter, HTTPException
from app.lib.utils import extract_images_from_pdf
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json

router = APIRouter()


class PDFBase64(BaseModel):
    base64: str


@router.post("/extract/images")
async def pdf_extract_images_stream(PdfBase64: PDFBase64):

    print(PdfBase64)

    try:
        data = json.loads(PdfBase64)
    except:
        raise HTTPException(status_code=400, detail="No PDF base64 provided")

    # Check if the base64 string is provided
    if not data.base64:
        raise HTTPException(status_code=400, detail="No PDF base64 provided")

    # Extract images from PDF
    images = extract_images_from_pdf(data.base64)

    response = JSONResponse(content={"images": images, "total": len(images)})

    return response
