from pydantic import BaseModel, EmailStr

class EmailDTO(BaseModel):
    recipient: EmailStr
    subject: str
    body: str
    mail_type: str
    language: str