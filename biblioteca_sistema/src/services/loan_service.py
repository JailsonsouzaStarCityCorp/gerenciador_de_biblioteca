from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import and_
from ..database.models import Loan, Book, User
from ..database.connection import db_connection


class LoanService:
    def __init__(self) -> None:
        self.session = db_connection.get_session()

    def create_loan(self, user_id: int, book_id: int, days: int = 14) -> Loan:
        user: Optional[User] = self.session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Usuário não encontrado")
        book: Optional[Book] = self.session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError("Livro não encontrado")
        if not book.is_available:
            raise ValueError("Livro não está disponível")
        loan = Loan(
            user_id=user_id,
            book_id=book_id,
            loan_date=datetime.now(),
            is_returned=False,
        )
        book.is_available = False
        self.session.add(loan)
        self.session.commit()
        self.session.refresh(loan)
        return loan

    def return_loan(self, loan_id: int) -> bool:
        loan: Optional[Loan] = self.session.query(Loan).filter(Loan.id == loan_id).first()
        if not loan or loan.is_returned:
            return False
        loan.is_returned = True
        loan.return_date = datetime.now()
        book: Optional[Book] = self.session.query(Book).filter(Book.id == loan.book_id).first()
        if book:
            book.is_available = True
        self.session.commit()
        return True

    def renew_loan(self, loan_id: int, extra_days: int = 7) -> bool:
        loan: Optional[Loan] = self.session.query(Loan).filter(Loan.id == loan_id).first()
        if not loan or loan.is_returned:
            return False
        # Simplesmente ajusta a loan_date para refletir renovação (sem due_date explícito)
        loan.loan_date = loan.loan_date + timedelta(days=extra_days)
        self.session.commit()
        return True

    def get_active_loans_by_user(self, user_id: int) -> List[Loan]:
        return self.session.query(Loan).filter(Loan.user_id == user_id, Loan.is_returned == False).all()

    def get_active_loans(self) -> List[Loan]:
        return self.session.query(Loan).filter(Loan.is_returned == False).all()

    def get_returned_loans(self) -> List[Loan]:
        return self.session.query(Loan).filter(Loan.is_returned == True).all()

    def get_user_history(self, user_id: int) -> List[Loan]:
        return self.session.query(Loan).filter(Loan.user_id == user_id).order_by(Loan.loan_date.desc()).all()

    def __del__(self) -> None:
        if hasattr(self, "session"):
            self.session.close()


