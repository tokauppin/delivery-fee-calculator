
## Running the project

run the command `pip install pytest flask` to install required dependencies

To run the pytests run the command `pytest`

In the root of the project run `python delivery_fee_API.py` to start the server 

Run `curl -X POST -H "Content-Type: application/json" -d "{\"cart_value\": 790, \"delivery_distance\": 2235, \"number_of_items\": 4, \"time\": \"2024-01-15T13:00:00Z\" }" http://127.0.0.1:5000` in a separate terminal to test the example request given in the assignment

You can remove keys or values from the request body to see input validation 

***

***
About the PYTESTS:

There are 9 different customer orders in test_API.py to test the rules for calculating a delivery fee. The tests covers the following scenarios:
- Small order surcharge
- Fee for the delivery distance (under and over 1000m)
- Fee for extra items and a bulk fee for orders with over 12 items
- The delivery fee is never over 15€
- Free delivery when cart value is at least 200€
- Friday rush hour 3-7pm has a surcharge

***

link to the assigment: https://github.com/woltapp/engineering-internship-2024