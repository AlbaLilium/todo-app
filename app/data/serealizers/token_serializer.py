from pydantic import BaseModel


class Token(BaseModel):
    """
    Token Serializer for authentication.

     ...

     Attributes
     ----------
      access_token: str
      type_token: str

    """

    access_token: str
    type_token: str


class TokenData(BaseModel):
    """
    Token data Serializer for authentication.

     ...

     Attributes
     ----------
      username: str | None = None

    """

    username: str | None = None
