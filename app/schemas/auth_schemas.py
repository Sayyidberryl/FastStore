from pydantic import BaseModel

class TokenRequest(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str
    