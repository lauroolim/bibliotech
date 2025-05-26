class Book:
    def __init__(self, id, title, isbn, publish_year=None, created_at=None, authors=None):
        self.id = id
        self.title = title
        self.isbn = isbn
        self.publish_year = publish_year
        self.created_at = created_at
        self.authors = authors or []

    @property
    def status_badge(self):
        return "success" if self.is_available else "danger"
    
    @property
    def status_text(self):
        return "Disponível" if self.is_available else "Emprestado"