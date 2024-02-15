# ContempoCrafts E-Commerce Application

## Application Showcase

### Homepage
![](homepage-display.png)

### Product Detail
![](product-detail-display.png)

### Checkout
![](checkout-display.png)

## Time Allocated
* 14 days to complete an MVP.

## Tech Stack
* Django
* PostgreSQL
* HTML
* CSS (Grid and Flexbox)
* Vanilla JavaScript / Document Object Model API

## Requirements
* Design and develop an E-Commerce MVP based on:
    * A bag system
      * Session-based storage to structure and organize products that will be purchased.
      * Track the quantity of each product item.
    * 3 different webpages
      * A homepage containing a list of products
        * Include basic information about the products such as
            the name and its rating.
      * A product detail page
        * Include all information on the detail page.
      * A Checkout page
        * Form for shipping and contact information
        * Displays to the user the contents of the bag (products and quantities)
        * When shipping and contact information are submitted
            * An order is made
    * Entities / Models
        * Order
        * Product
        * OrderItem (intermediary table)

## Implementation
* Bag/Checkout System
    * JavaScript (ShoppingBagUtil.js)
        * Dynamically updates the number of products in the bag.
        * Sends the product ID of a particular product to a Django view when \
        the "Add To Bag" button is clicked on the home or product detail page via AJAX.
    * Django (add-to-bag view)
        * Consumes the product ID sent from AJAX request and stores it in a user session.
        * A session object and custom context processor to make the bag quantity available on all web pages via the key "total_items".
*  Views
    * Homepage
        * IndexView (displays a maximum of 6 products)
    * Product Detail
        * Detail View
    * Checkout
        * Standard function-based view.
            * Pulls products and quantities stored from \
            the session in a dictionary called "bag".
                * "Bag" is a list of dictionaries containing \
                product IDs and quantities of each product.
                * Contextualizes the "bag" into a new list \
                containing the product model objects, \
                the quantity of each product, and \
                the image of the product.
            * Calculates the total cost of all items to
                * Display it in the view.
                * Eventually save it in the order model object.
            * Manages the ModelForm (associated with Order) on the view.
            * Redirects the end users to the home page \
            when a form is submitted and a new order is created. \
            A message from django.contrib.messages is displayed confirming the order.
* Models / Entities
    * Product
        * Fields
            * name
            * rating (MinValueValidator(0) and MaxValueValidator(10))
            * price (max_digits=5, decimal_places=2)
            * description
            * image
    * Order
        * Fields
            * products (M2M relationship)
            * total_cost
            * first_name
            * last_name
            * email
            * phone_number (RegexValidator r'^\d{3}-\d{3}-\d{4}$')
            * street
            * zip
            * city
            * state
    * OrderItem (intermediary table)
        * Fields
            * product (FK)
            * order (FK)
            * quantity

## Potential Enhancements
* Add the ability to remove products or modify the quantity in the bag.
* Implement a payment system such as Stripe.
* Account-oriented orders (make orders accessible in user profiles / allow guests).
* Improve application accessibility for assistive technologies.
* Add an "About Us" page to make use of the anchor tag in the navigation bar.
* Pagination

## Learning Curves
* Handling image files that aren't scriptable (iterating over lists or dictionaries with images in them).
    - Reference get_products_and_quantities_from_bag function in store/views.py.
* AJAX integration with Django views (design, development, and making use of CSRF tokens).
    - JavaScript: ShoppingBagUtil.js
    - Django: add-to-bag view
* Django sessions
* Test Driven Development (TDD) (Python)
* Making practical use of Many-To-Many relationships.
* Adding the total cost of an order after the model object is created and when its attribute/field has constraints on it.

# Areas To Improvement In
* I think I could've done better with balancing clean code practices and documentation. 
    * Writing enough documentation that it isn't redundant but also ensuring it's there when deemed necessary.
* TDD in JavaScript via Jest.
* Research and learn more about best practices on
    * Handling test images
    * Designing and developing complicated views that may need one or more helper methods.
    * How to make better use of methods like in store/tests/utils.py
        * Develop a better understanding of how to integrate functions or methods that create model objects and other setUp related tasks to reduce redundancy.
* Apply normalization rules to the Order model.
    * It currently serves as a model for both shipping info and contact information so the fields should be split into more than one.
* Learn how to position the product quantity next to the bag icon.
