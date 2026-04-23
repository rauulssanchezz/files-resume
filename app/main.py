from fastapi import FastAPI, UploadFile, HTTPException, status
import os
from groq import Groq

app = FastAPI(
    title="Files Resume Api"
)

@app.post("/resume-file")
async def resume_file(file: UploadFile):
   if file.content_type != "text/plain":
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="El archivo solo puede conter texto"
        )
   return await file.read()