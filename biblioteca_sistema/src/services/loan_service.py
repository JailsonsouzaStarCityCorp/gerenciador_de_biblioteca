from typing import List
from ..database.models import Loan
from ..database.connection import db_connection


class LoanService:
    def __init__(self) -> None:
        self.session = db_connection.get_session()

    def get_active_loans_by_user(self, user_id: int) -> List[Loan]:
        return self.session.query(Loan).filter(Loan.user_id == user_id, Loan.is_returned == False).all()

    def __del__(self) -> None:
        if hasattr(self, "session"):
            self.session.close()


