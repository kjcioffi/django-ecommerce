class BagSystem {
    constructor() {
        this._addToBagBtn = document.querySelectorAll('#add-to-bag');
        this._addToBagBtn.forEach(button => button.addEventListener('click', () => {
            const product_id = button.getAttribute('product-id');
            this.sendProductIdToDjango(product_id);
        }))
    };

    /**
     * Sends the ID of a product to Django's backend for \
     * processing and storing product item data in session storage.
     * @param {string} product_id 
     */
    async sendProductIdToDjango(product_id) {
        await fetch('/add-to-bag/', {
            method: "POST",
            headers: {
                "X-CSRFToken": this.getCookie('csrftoken'),
                "Content-Type": 'application/x-www-form-urlencoded' 
            },
            body: 'product_id=' + product_id
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Success!');
            }
        });
    };

    /**
     * Retrieves cookies from the browser.
     * Credit to the Django documentation for this method.
     * https://docs.djangoproject.com/en/5.0/howto/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
     * TO-DO: simply this by using the js-cookie library via NPM.
     * @param {string} name 
     * @returns
     */
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
}

new BagSystem();