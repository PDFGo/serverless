from fastapi import APIRouter, HTTPException
from app.lib.utils import extract_images_from_pdf
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

router = APIRouter()


class PDFBase64(BaseModel):
    base64: str


@router.post("/extract/images/")
async def pdf_extract_images_stream(PdfBase64: PDFBase64):

    # parse the request body
    try:
        data = jsonable_encoder(PdfBase64)
    except:
        raise HTTPException(status_code=400, detail="No PDF base64 provided")

    # Check if the base64 string is provided
    if not data['base64']:
        raise HTTPException(status_code=400, detail="No PDF base64 provided")

    # Extract images from PDF
    try:
        images = extract_images_from_pdf(data['base64'])
        res = {"message": "Images extracted successfully", "status": "success",
               "code": 200,
               "total": len(images),
               "images": images
               }
        return res
    except:
        raise HTTPException(
            status_code=400, detail="Error extracting images from PDF")


# Dictionary to store connected clients
# connected_clients: Dict[str, WebSocket] = {}


# @router.websocket("/ws/{client_id}")
# async def websocket_endpoint(client_id: str, websocket: WebSocket):
#     await websocket.accept()

#     # Add the client's WebSocket connection to the dictionary
#     connected_clients[client_id] = websocket

#     try:
#         while True:
#             # Wait for incoming data from the client
#             data = await websocket.receive_text()

#             # Process the received data here if needed

#             # Send a response back to the client (optional)
#             await websocket.send_text(str(data))
#     except WebSocketDisconnect:
#         # Remove the disconnected client from the dictionary
#         del connected_clients[client_id]
#         await websocket.close()


# Broadcast message to all connected clients
# async def broadcast_message(message: str):
#     for client_id, websocket in connected_clients.items():
#         try:
#             await websocket.send_text(message)
#         except Exception:
#             # Remove disconnected clients from the dictionary
#             del connected_clients[client_id]


# @router.post("/extract/images/ws")
# async def broadcast_to_client(Item: Payload):
#     data = jsonable_encoder(Item)
#     # Extract images from PDF
#     images = extract_images_from_pdf(data['base64'])

#     if data['client_id']:
#         # Send message to a specific client
#         websocket = connected_clients.get(data['client_id'])
#         if not websocket:
#             raise HTTPException(
#                 status_code=400, detail="Specified client is not connected")
#           # Upload images to S3

#         images = set(images)
#         images = list(images)

#         for image in images:
#             url = upload_base64_image_to_s3(
#                 'pdf-expert',  f'{data["client_id"]}/image_{images.index(image)}.jpeg', image)
#             res = {
#                 "url": url,
#                 'message': "Image uploaded successfully",
#                 'status': 'success',
#                 'code': 200,
#                 'total': len(images),
#                 'client_id': data['client_id']
#             }
#             await websocket.send_text(str(res))
#             await asyncio.sleep(1)
#         return {"message": "Message sent"}
#     else:
#         # Send message to all connected clients
#         await broadcast_message({
#             "message": "Message sent to all connected clients"
#         })
#         return {"message": "Message sent"}
