# ContempoCrafts E-Commerce Application

## Project Overview

### A craftsmen, are you?

***Turn your passion*** and experience with the art of making **into a side hustle**. ContempoCrafts is a online platform (Software as a Service) that sells your handcrafted goods in minutes.

Simply setup and manage the store, we'll handle the rest. From payments and sales reports to the website hosting.

# Running ContempoCrafts locally

1. **Clone the repository**:

    ```bash
    git clone [repository-url]
    cd django-ecommerce
    ```

2. **Create Stripe account**:

    i. Create your Stripe account: <https://dashboard.stripe.com/register>

    ii. Create an API key <`STRIPE_API_KEY`>: <https://dashboard.stripe.com/test/apikeys>

    iii. Create a Webhook with a key <`STRIPE_WEBOOK_KEY`>: <https://dashboard.stripe.com/test/apikeys>

3. **Set up environment variables:**

    ```
    mv .env-template .env
    ```

    *Fill in the environment file with the required variables.*

    **An optional way to create a Django secret key**:
    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

4. **(Recommended) Create a virtual environment:**

    ```bash
    python -m pip install pip-tools
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

5. **Install dependencies:**

    ```bash
    pip-sync requirements\prod\requirements.txt requirements\dev-requirements.txt
    ```

6. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

You should now be able to access the application at <http://localhost:8000>.
