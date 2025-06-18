from fastapi import FastAPI, UploadFile, File
from fastui import FastUI, components as c

app = FastAPI()

@app.get("/", response_model=FastUI, response_model_exclude_none=True)
def home():
    return [
        c.Page(
            components=[
                c.Heading(text="Chat Bot", level=2),
                c.Text(text="Hello! How can I help you?"),
                c.FileUpload(name="file"),
                c.Button(text="Send")
            ]
        )
    ]

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"filename": file.filename}

# Run with: uvicorn app:app --reload 