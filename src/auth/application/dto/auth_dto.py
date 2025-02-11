from pydantic import BaseModel, EmailStr

class LoginDTO(BaseModel):
    """DTO for login requests"""
    email: EmailStr

class TokenResponseDTO(BaseModel):
    """DTO for token responses"""
    access_token: str
    token_type: str = "bearer" 