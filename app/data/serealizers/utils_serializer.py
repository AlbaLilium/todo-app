from pydantic import BaseModel


class Pagination(BaseModel):
    """
      Pagination Serializer.

       ...

       Attributes
       ----------
        page_size: int
        page_number: int

    """
    page_size: int
    page_number: int
