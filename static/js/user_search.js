class UserSearch extends SearchBase {
    constructor(options = {}) {
        const defaults = {
            searchInputId: 'user_search',
            searchButtonId: 'searchUserBtn',
            resultContainerId: 'userResult',
            hiddenInputId: 'user_id',
            placeholder: 'Digite email do usuário'
        };
        super({...defaults, ...options});
    }

    formatResult(user) {
        return `<strong>${user.username}</strong> - ${user.email}`;
    }
}