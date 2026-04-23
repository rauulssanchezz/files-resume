from fastapi import BackgroundTasks, FastAPI, UploadFile, HTTPException, status
import os
from fastapi.responses import FileResponse
from groq import AsyncGroq
from dotenv import load_dotenv

from app.schema import CreateFileData

load_dotenv()

client = AsyncGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

app = FastAPI(
    title="Files Resumer Api"
)

async def complete_chat(system_content: str, user_content: str) -> str:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "name": "File Resumer",
                "content": system_content
            },
            {
                "role": "user",
                "content": user_content,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    if chat_completion.choices[0].message.content is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ha ocurrido un error inesperado."
        )

    return chat_completion.choices[0].message.content

def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.post("/resume-file")
async def resume_file(file: UploadFile):
    try:
        if file.content_type != "text/plain":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo solo puede conter texto"
            )

        file_content = await file.read()

        chat_content = await complete_chat(
            system_content="Te encargas de resumir el contenido de los archivos localizando los puntos mas importantes.",
            user_content=f"Resume este texto: {file_content} "
        )

        return chat_content
    except:
        raise

@app.post("/create-extense-file")
async def create_extense_file(
    file: CreateFileData,
    background_tasks: BackgroundTasks
):
    try:
        chat_content = await complete_chat(
            system_content="Te encargas de apartir de un resumen, desarrollar el contenido y crear un contenido más extenso.",
            user_content=f"Desarrolla este tema: {file.resume}"
        )

        file_path = f"{file.file_name}.txt"

        with open(file_path, "w", encoding="utf-8") as new_file:
            new_file.write(chat_content)

        background_tasks.add_task(delete_file, file_path)

        return FileResponse(
            filename=file_path,
            path=file_path,
            media_type="text/plain"
        )
    except:
        raise