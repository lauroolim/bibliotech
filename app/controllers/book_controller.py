from app.services.book_service import BookService
from flask import render_template, request, redirect, url_for, flash
class BookController:
    def __init__(self, book_service: BookService):
        self.book_service = book_service

    def register_book(self):
        if request.method == 'POST':
            title = request.form['title']
            isbn = request.form['isbn']
            publish_year = request.form.get('publish_year')
            author_ids = request.form.getlist('author_ids')
            
            if publish_year:
                try:
                    publish_year = int(publish_year)
                except ValueError:
                    flash('Ano de publicação deve ser um número', 'danger')
                    authors = self.book_service.get_all_authors()
                    return render_template('admin/register_book.html', authors=authors)

            try:
                self.book_service.register_book(title, isbn, publish_year, author_ids)
                flash('Livro cadastrado com sucesso', 'success') 
                return redirect(url_for('admin.register_book'))  
            except ValueError as e:
                flash(str(e), 'danger')
                
        authors = self.book_service.get_all_authors()
        return render_template('admin/register_book.html', authors=authors)

    def register_author(self):
        if request.method == 'POST':
            full_name = request.form['full_name']
            
            try:
                self.book_service.register_author(full_name)
                flash('Autor cadastrado com sucesso', 'success')
                return redirect(url_for('admin.register_author'))
            except ValueError as e:
                flash(str(e), 'danger')
                
        return render_template('admin/register_author.html')

    def list_books(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int) 
        search = request.args.get('search', '', type=str)

        try:
            pagination = self.book_service.list_books(page, per_page, search)
            return render_template('admin/list_books.html', **pagination)
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('admin.dashboard'))

    def search_book_by_isbn(self, isbn):
        try:
            book = self.book_service.search_by_isbn(isbn)
            return book
        except ValueError as e:
            raise ValueError(str(e))

    def get_book_by_id(self, book_id):
        try:
            book = self.book_repository.fetch_book_by_id(book_id)
            if not book:
                raise ValueError("Livro não encontrado")
                
            if self.loan_repository:
                book.is_available = self.loan_repository.is_book_available(book.id)
                book.available_copies = 1 if book.is_available else 0
                book.total_copies = 1
            return book
        except Exception as e:
            raise ValueError(str(e))