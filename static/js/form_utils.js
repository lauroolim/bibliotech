class FormUtils {
    static setDefaultDate(inputId, daysFromNow = 14) {
        const input = document.getElementById(inputId);
        if (input) {
            const date = new Date(Date.now() + (daysFromNow * 24 * 60 * 60 * 1000));
            input.value = date.toISOString().split('T')[0];
        }
    }

    static validateForm(fieldIds, buttonId) {
        const isValid = fieldIds.every(id => document.getElementById(id)?.value.trim());
        const button = document.getElementById(buttonId);
        if (button) button.disabled = !isValid;
        return isValid;
    }
}