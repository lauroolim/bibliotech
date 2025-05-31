from app.services.book_service import BookService
from flask import render_template, request, redirect, url_for, flash
from app.utils.decorators import handle_controller_errors

class BookController:
    def __init__(self, book_service: BookService):
        self.book_service = book_service

    @handle_controller_errors('admin.register_book')
    def register_book(self):
        if request.method == 'POST':
            title = request.form['title']
            isbn = request.form['isbn']
            publish_year = request.form.get('publish_year')
            author_ids = request.form.getlist('author_ids')
            
            if publish_year:
                publish_year = int(publish_year)

            self.book_service.register_book(title, isbn, publish_year, author_ids)
            flash('Livro cadastrado com sucesso', 'success') 
            return redirect(url_for('admin.list_book'))  
                
        authors = self.book_service.get_all_authors()
        return render_template('admin/register_book.html', authors=authors)

    @handle_controller_errors('admin.register_author')
    def register_author(self):
        if request.method == 'POST':
            full_name = request.form['full_name']
            

            self.book_service.register_author(full_name)
            flash('Autor cadastrado com sucesso', 'success')
            return redirect(url_for('admin.register_author'))
                
        return render_template('admin/register_author.html')

    @handle_controller_errors('admin.list_books')
    def list_books(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int) 
        search = request.args.get('search', '', type=str)

        pagination = self.book_service.list_books(page, per_page, search)
        return render_template('admin/list_books.html', **pagination)

    def search_book_by_isbn(self, isbn):
        book = self.book_service.search_by_isbn(isbn)
        return book

    def get_book_by_id(self, book_id):
        book = self.book_service.get_book_by_id(book_id)
        if not book:
            raise ValueError("Livro não encontrado")

        return book