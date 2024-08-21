from app.db.db_connection import SessionLocal


class BaseOperation:
    def __enter__(self):
        self.session = SessionLocal()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.session.commit()
        except exc_type:
            self.session.rollback()
        finally:
            self.session.close()
