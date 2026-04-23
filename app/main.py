from fastapi import FastAPI, UploadFile, HTTPException, status
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

app = FastAPI(
    title="Files Resumer Api"
)

@app.post("/resume-file")
async def resume_file(file: UploadFile):
    if file.content_type != "text/plain":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo solo puede conter texto"
        )

    file_content = await file.read()
   
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "name": "File Resumer",
                "content": "Te encargas de resumir el contenido de los archivos localizando los puntos mas importantes."
            },
            {
                "role": "user",
                "content": f"Resume este texto: {file_content} ",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content