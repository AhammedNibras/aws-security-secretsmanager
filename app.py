import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import your temporary, hard-coded credentials
import config

app = FastAPI()

# Mount static files so /static/style.css is served
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_index():
    """
    Serve a simple landing page (index.html).
    """
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/buckets")
def list_s3_buckets():
    """
    Demonstrates why we need AWS credentials:
    This endpoint lists the user's S3 buckets behind the scenes.
    Initially, it uses hard-coded credentials from config.py.
    """
    try:
        session = boto3.Session(
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_REGION
        )
        s3 = session.client("s3")
        response = s3.list_buckets()

        bucket_names = [bucket["Name"] for bucket in response.get("Buckets", [])]
        return JSONResponse(content={"buckets": bucket_names})

    except ClientError as e:
        # Return the error in JSON for clarity
        return JSONResponse(content={"error": str(e)}, status_code=400)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
