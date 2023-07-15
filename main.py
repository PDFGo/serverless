from fastapi import FastAPI
# from mangum import Mangum
from app.routes import pdf

app = FastAPI()
# handler = Mangum(app, lifespan="off")

app.include_router(pdf.router, prefix="/api/v1/pdf", tags=["pdf"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
