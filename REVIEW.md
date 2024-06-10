# Django Ecommerce Review

## General
- pip install -r requirements.txt not working because of psycopg2-binary needed for mac
- For the database I would mention the use of sqlite in the readme to test quickly the project instead of having to install a postgresql server specially to test the project
- Good to see a context processor there, do you need to add tests for it?
- Use black for fix code style automatically
- Create utils file to contain business logic function (views should be as simple, readable as possible)
## Ecommerce

## Store
views:
    - Replace function based views by class based views
    - Business logic should be stored in functions in a utils file instead of being directly in the view
    - Rename class Index(ListView): to something more meaningful like ProductListView
    - Rename index.html to product_list.html
    - In your tests, think about organising the sections [prerequisites, call to function to test, assertions]
    - Please [factory boy](https://factoryboy.readthedocs.io/en/stable/) to create fake products for your tests instead of creating a utils method in your tests folder directly
    - creating a util function for your tests is dangerous because this function is not covered by tests and if something is broken in this function then the tests will fail
    - User [faker](https://faker.readthedocs.io/en/master/) to create fake data for your tests
    - organise your tests in folder per layer
    - test_product_quantity_successfully_associates_with_an_order, please use factory boy to generate fake data
    - what is the goal of this function validate_rating?
    - Add suffix for your test for example TestRegisterView, TestRegisterModel 
