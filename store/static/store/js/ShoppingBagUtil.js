/**
 * Assists Django in adding products to a user's shopping bag \
 * by communicating with Django's backend to store and process product information.
 *
 * Usage:
 * The class automatically binds click event listeners to elements with the 
 * 'add-to-bag' ID and handles the subsequent POST requests to the Django server.
 */
class ShoppingBagUtil {
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
        try {
            const response = await fetch('/add-to-bag/', {
                method: "POST",
                headers: {
                    "X-CSRFToken": this.getCookie('csrftoken'),
                    "Content-Type": 'application/x-www-form-urlencoded' 
                },
                body: 'product_id=' + product_id
            });

            if (!response.ok) {
                throw new Error(`Http error! status: ${response.status}`)
            }

            const data = await response.json();
            if (data.status === 'success') {
                this.updateBagQuantity(data.total_items);
            } else {
                console.error('Error with request: ', data);
            }
        } catch(error) {
            console.error('There was a problem with the fetch operation: ', error.message);
        }
    };

    /**
     * Retrieves cookies from the browser.
     * Credit to the Django documentation for this method.
     * https://docs.djangoproject.com/en/5.0/howto/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
     * TO-DO: simplify this by using the js-cookie library via NPM.
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

    updateBagQuantity(payload) {
        // TO-DO: fix caching issue that causes the previous known \
        // quantity to appear on the page due to back button clicks.
        const bagQuantityElement = document.querySelector('.bag-quantity');
        bagQuantityElement.textContent = payload.toString();
    }
}

new ShoppingBagUtil();