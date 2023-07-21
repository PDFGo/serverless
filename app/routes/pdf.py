from fastapi import APIRouter, HTTPException, Response
from app.lib.utils import extract_images_from_pdf
from pydantic import BaseModel
from fastapi.responses import JSONResponse, StreamingResponse
import json

router = APIRouter()


class PDFBase64(BaseModel):
    base64: str


@router.post("/extract/images")
async def pdf_extract_images_stream(PdfBase64: PDFBase64):
    # Check if the base64 string is provided
    if not PdfBase64.base64:
        raise HTTPException(status_code=400, detail="No PDF base64 provided")

    # Return the extracted image
    return StreamingResponse(extract_images_from_pdf(PdfBase64.base64), media_type="application/json")
