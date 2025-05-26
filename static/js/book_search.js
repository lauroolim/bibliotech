class BookSearch extends SearchBase {
    constructor(options = {}) {
        const defaults = {
            searchInputId: 'book_search',
            searchButtonId: 'searchBookBtn',
            resultContainerId: 'bookResult',
            hiddenInputId: 'book_id',
            placeholder: 'Digite ISBN do livro'
        };
        super({...defaults, ...options});
        
        this.availabilityUrl = options.availabilityUrl;
        this.checkAvailability = options.checkAvailability !== false;
    }

    async handleResult(book) {
        if (this.checkAvailability && this.availabilityUrl) {
            await this.checkBookAvailability(book);
        } else {
            this.displayResult(book);
        }
    }

    async checkBookAvailability(book) {
        try {
            const response = await fetch(`${this.availabilityUrl}?book_id=${book.id}`);
            const availability = await response.json();
            
            this.displayBookWithAvailability(book, availability);
        } catch (error) {
            console.error('Erro ao verificar disponibilidade:', error);
            this.displayBookWithAvailability(book, { available: false, error: 'Erro ao verificar' });
        }
    }

    displayBookWithAvailability(book, availability) {
        const hiddenInput = document.getElementById(this.hiddenInputId);
        const bookInfo = this.formatResult(book);
        
        if (availability.available) {
            this.showAlert('success', `${bookInfo}<br><small class="text-success">✓ Disponível</small>`);
            hiddenInput.value = book.id;
        } else {
            const msg = availability.error || 'Já está emprestado';
            this.showAlert('warning', `${bookInfo}<br><small class="text-danger">✗ ${msg}</small>`);
            hiddenInput.value = '';
        }
        
        if (this.onSelected) {
            this.onSelected(book, availability.available, availability);
        }
    }

    formatResult(book) {
        return `<strong>${book.title}</strong> - ISBN: ${book.isbn}`;
    }
}