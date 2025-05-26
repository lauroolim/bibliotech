class SearchBase {
    constructor(options = {}) {
        this.searchInputId = options.searchInputId || 'search_input';
        this.searchButtonId = options.searchButtonId || 'search_btn';
        this.resultContainerId = options.resultContainerId || 'search_result';
        this.hiddenInputId = options.hiddenInputId || 'selected_id';
        this.searchUrl = options.searchUrl;
        this.placeholder = options.placeholder || 'Digite para buscar...';
        this.onSelected = options.onSelected || null;
        
        console.log('SearchBase initialized with:', options);
        this.init();
    }

    init() {
        const searchBtn = document.getElementById(this.searchButtonId);
        const searchInput = document.getElementById(this.searchInputId);
        
        console.log('Init - Button:', searchBtn, 'Input:', searchInput);
        
        if (searchBtn) {
            searchBtn.addEventListener('click', () => {
                console.log('Search button clicked');
                this.performSearch();
            });
        }
        
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    console.log('Enter key pressed');
                    this.performSearch();
                }
            });
            searchInput.placeholder = this.placeholder;
        }
    }

    performSearch() {
        const searchTerm = document.getElementById(this.searchInputId).value.trim();
        console.log('Performing search for:', searchTerm);
        
        if (!searchTerm) {
            alert(this.placeholder);
            return;
        }
        this.search(searchTerm);
    }

    async search(searchTerm) {
        console.log('Searching with URL:', this.searchUrl, 'Term:', searchTerm);
        
        try {
            const url = `${this.searchUrl}?term=${encodeURIComponent(searchTerm)}`;
            console.log('Full URL:', url);
            
            const response = await fetch(url);
            const data = await response.json();
            
            console.log('Search response:', data);
            
            if (data.error) {
                this.showAlert('warning', data.error);
                this.clearSelection();
            } else {
                await this.handleResult(data);
            }
        } catch (error) {
            console.error('Erro na busca:', error);
            this.showAlert('danger', 'Erro na busca. Tente novamente.');
            this.clearSelection();
        }
    }

    async handleResult(data) {
        console.log('Base handleResult called with:', data);
        this.displayResult(data);
    }

    displayResult(data) {
        console.log('Displaying result:', data);
        const hiddenInput = document.getElementById(this.hiddenInputId);
        
        this.showAlert('success', this.formatResult(data));
        hiddenInput.value = data.id;
        
        if (this.onSelected) {
            this.onSelected(data);
        }
    }

    formatResult(data) {
        return `<strong>${data.name || data.title || data.username}</strong>`;
    }

    showAlert(type, message) {
        console.log('Showing alert:', type, message);
        const resultContainer = document.getElementById(this.resultContainerId);
        
        if (!resultContainer) {
            console.error('Result container not found:', this.resultContainerId);
            return;
        }
        
        const iconMap = {
            'success': 'check-circle',
            'warning': 'exclamation-triangle',
            'danger': 'x-circle'
        };
        
        resultContainer.innerHTML = `
            <div class="alert alert-${type}">
                <i class="bi bi-${iconMap[type]}"></i> ${message}
            </div>
        `;
    }

    clearSelection() {
        const hiddenInput = document.getElementById(this.hiddenInputId);
        if (hiddenInput) {
            hiddenInput.value = '';
        }
    }

    clear() {
        document.getElementById(this.searchInputId).value = '';
        document.getElementById(this.resultContainerId).innerHTML = '';
        document.getElementById(this.hiddenInputId).value = '';
    }

    getValue() {
        return document.getElementById(this.hiddenInputId).value;
    }
}