from fastapi import FastAPI

app = FastAPI(
    title="Files Resume Api"
)

@app.get("/")
def hello_world():
    return "Hola mundo"