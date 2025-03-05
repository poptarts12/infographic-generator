from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(title="Infographic Generator")

# Serve static files (CSS, JS, assets)
app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

# Serve the main HTML file at "/"
@app.get("/")
async def serve_index():
    index_path = os.path.join("frontend", "index.html")
    return FileResponse(index_path)

# Run the server
if __name__ == "__main__":
    print("🚀 Starting FastAPI Server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
