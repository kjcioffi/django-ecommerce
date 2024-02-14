# ContempoCrafts E-Commerce Application

## Tech Stack
* Django
* HTML
* CSS (Grid and Flexbox)
* Vanilla JavaScript

## Requirements
* Design and develop an E-Commerce MVP based on:
    * A bag system
      * Session based storage to structure and organize products \
      that will be purchased.
      * Track quantity of each product item.
    * 3 different webpages
      * A homepage containing a list of products
        * Include basic information about the products such as
            the name and it's rating.
      * A product detail page
        * Include all information in the detail page.
      * A Checkout page
        * Form for shipping and contact information
        * Displays to the user the contents of the bag (products and quantities)
        * When shipping and contact information is submitted
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
        * Consumes the product ID sent by JavaScript AJAX and stores it in a user session.
        * A session object and custom context processor to make the bag quantity available on all web pages via the key "total_items".
* Views
    * Homepage
        * IndexView (displays a maximum of 6 products)
    * Product Detail
        * Detail View
    * Checkout
        * Standard function based view.
            * Pulls products and quantities stored from \
            the session called "bag".
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
            A message from django.contrib.messages is also displayed confirming the order.
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
                