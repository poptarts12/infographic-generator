from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from contextlib import asynccontextmanager

# Import ChatManager
import chat_manager

# Import API routers
from routes.generate import router as generate_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    app.state.chat_manager = chat_manager.ChatManager()
    
    # The application runs while we're "yielded" here
    yield
    
    # Shutdown logic (if needed)
    # e.g. close database connections, etc.

# Initialize FastAPI app with the lifespan context
app = FastAPI(
    title="Infographic Generator",
    lifespan=lifespan
)

# Serve static files (CSS, JS)
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")

# Serve the main HTML file at "/"
@app.get("/")
async def serve_index():
    index_path = os.path.join("frontend", "index.html")
    return FileResponse(index_path)

# Include API routers (ensures endpoints work)
app.include_router(generate_router, prefix="/api")

# Mount the "generated" folder at the route "/generated"
app.mount("/generated", StaticFiles(directory="generated"), name="generated")

if __name__ == "__main__":
    port = 8000
    print(f"🚀 Starting FastAPI Server at http://127.0.0.1:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

