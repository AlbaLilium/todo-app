from sqlalchemy.orm import Query

from app.db.db_connection import AsyncSession


class BaseOperation:
    async def __aenter__(self):
        self.session = AsyncSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.session.commit()
        except exc_type:
            await self.session.rollback()
        finally:
            await self.session.close()

    @staticmethod
    def paginate(query: Query, page_size: int, page_number: int) -> Query:
        return query.limit(page_size).offset(page_size * (page_number - 1))
