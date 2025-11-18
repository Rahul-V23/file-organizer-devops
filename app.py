from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import shutil
import os
from organizer import organize_files

app = FastAPI(
    title="File Organizer – Live Demo",
    description="Upload any files → watch them get auto-sorted instantly",
    version="1.0"
)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
      <head><title>File Organizer Live Demo</title></head>
      <body style="font-family: Arial; text-align: center; margin-top: 50px;">
        <h1>File Organizer – Live Demo</h1>
        <p>Upload files → they get auto-sorted into folders instantly</p>
        <form action="/organize" enctype="multipart/form-data" method="post">
          <input name="files" type="file" multiple style="font-size: 18px;">
          <br><br>
          <button type="submit" style="font-size: 18px; padding: 10px 20px;">Organize Now!</button>
        </form>
        <p><small>Powered by Docker + AWS Fargate + GitHub Actions</small></p>
      </body>
    </html>
    """


@app.post("/organize")
async def organize(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(400, "No files uploaded")

    # Clean + create folders
    for folder in ["incoming", "watch_folder"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    # Save uploaded files
    for file in files:
        path = f"watch_folder/{file.filename}"
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    # Run your original organizer
    organize_files()

    return {
        "status": "success",
        "message": f"Organized {len(files)} file(s)!",
        "sorted_into": [d for d in os.listdir("watch_folder") if os.path.isdir(f"watch_folder/{d}")]
    }