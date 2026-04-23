from pydantic import BaseModel, Field

class CreateFileData(BaseModel):
    file_name: str = Field(min_length=1, max_length=10)
    resume: str = Field(min_length=1, max_length=500)