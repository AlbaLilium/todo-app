from fastapi.security import HTTPBearer, OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()