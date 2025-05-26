from datetime import date

class Loan:
    def __init__(self, id, created_at, expected_return_date, returned_at=None, 
                 book_id=None, user_id=None, employee_id=None, status='ativo',
                 book=None, user=None, employee=None):

        self.id = id
        self.created_at = created_at
        self.expected_return_date = expected_return_date
        self.returned_at = returned_at
        self.book_id = book_id
        self.user_id = user_id
        self.employee_id = employee_id
        self.status = status
        self.book = book
        self.user = user
        self.employee = employee

    @property
    def is_overdue(self):
        if self.returned_at:
            return False
        return date.today() > self.expected_return_date

    @property
    def is_active(self):
        return self.returned_at is None

    @property
    def is_returned(self):
        return self.returned_at is not None

    def days_overdue(self):
        if not self.is_overdue:
            return 0
        return (date.today() - self.expected_return_date).days

    def mark_as_returned(self, return_date=None):
        if return_date is None:
            return_date = date.today()
        self.returned_at = return_date
        self.status = 'encerrado'

    def mark_as_overdue(self):
        if not self.returned_at and date.today() > self.expected_return_date:
            self.status = 'atrasado'

    def __repr__(self):
        return f"<Loan(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status={self.status})>"