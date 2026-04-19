from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    init_data: str = Field(..., min_length=1, max_length=8192)


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., min_length=20, max_length=512, pattern=r"^[A-Za-z0-9_\-]+$")


class LogoutRequest(BaseModel):
    refresh_token: str = Field(..., min_length=1, max_length=512)


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    expires_at: int
    refresh_expires_at: int


class LogoutResponse(BaseModel):
    revoked: bool
