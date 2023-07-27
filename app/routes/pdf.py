from fastapi import APIRouter, HTTPException
from app.lib.utils import extract_images_from_pdf, upload_base64_image_to_s3
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
# from dotenv import load_dotenv
from fastapi.responses import StreamingResponse


router = APIRouter()


class PDFBase64(BaseModel):
    base64: str


# Load environment variables from config.env
# load_dotenv("config.env")


@router.post("/extract/images")
async def pdf_extract_images_stream(PdfBase64: PDFBase64):

    # parse the request body
    try:
        data = jsonable_encoder(PdfBase64)
    except:
        raise HTTPException(status_code=400, detail="No PDF base64 provided")

    # Check if the base64 string is provided
    if not data['base64']:
        raise HTTPException(status_code=400, detail="No PDF base64 provided")

    # function
    async def generate_data():
        # Extract images from PDF
        images = extract_images_from_pdf(data['base64'])

        # Upload images to S3
        i = 0
        for image in images:
            url = upload_base64_image_to_s3(
                'pdf-expert',  f'new/test_{images.index(image)}.jpeg', image)
            i += 1
            res = {
                "url": url,
                'message': "Image uploaded successfully",
                'status': 'success',
                'code': 200,
                'total': len(images),
            }
            print(res)
            # yield b"Data " + str(res).encode() + b"\n"
            yield str(res).encode() + b"\n"

    return StreamingResponse(generate_data())
