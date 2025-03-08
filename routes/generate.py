from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel
import uuid
import glob
import os

router = APIRouter()

class InfographicRequest(BaseModel):
    text: str

def background_process_job(chat_manager, job_id, text):
    # Process the job in the background
    chat_manager.process_job(job_id, text)

@router.post("/generate")
async def generate_infographic(background_tasks: BackgroundTasks, request: Request, req_body: InfographicRequest):
    folder_path = "generated"
    for file_path in glob.glob(os.path.join(folder_path, "*.svg")):
        os.remove(file_path)
    chat_manager = request.app.state.chat_manager  # Get global ChatManager instance
    job_id = str(uuid.uuid4())  # Generate a unique job ID
    
    # Add the job to be processed in the background
    background_tasks.add_task(background_process_job, chat_manager, job_id, req_body.text)
    
    return {"job_id": job_id, "status": "working on it"}

@router.get("/status/{job_id}")
async def get_status(job_id: str, request: Request):
    chat_manager = request.app.state.chat_manager
    return {"job_id": job_id, "status": chat_manager.get_status(job_id)}

@router.get("/result/{job_id}")
async def get_result(job_id: str, request: Request):
    chat_manager = request.app.state.chat_manager
    result = chat_manager.get_result(job_id)  # Get the final result (e.g., image URL)
    if not result:
        # If result is not ready, return a message indicating that
        return {"job_id": job_id, "status": "result not ready yet"}
    return {"job_id": job_id, "status": "completed", "result": result}
