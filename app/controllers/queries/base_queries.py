from sqlalchemy.orm import Query

from app.db.db_connection import SessionLocal


class BaseOperation:
    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.session.commit()
        except exc_type:
            self.session.rollback()
        finally:
            self.session.close()

    @staticmethod
    def paginate(query: Query, page_size: int, page_number: int) -> Query:
        return query.limit(page_size).offset(page_size * (page_number - 1))
