
from flask import Flask, request, jsonify
from datetime import datetime

MINIMUM_ORDER = 1000                 # cents
LIMIT_FOR_FREE_DELIVERY = 20_000     # cents
BASE_DELIVERY_FEE = 200              # cents
MAX_DELIVERY_FEE = 1500              # cents
DISTANCE_FOR_BASE_FEE = 1000         # metres
SURCHARGE_ITEM_LIMIT = 4             # number of items


def friday_rush(order_time: str) -> bool:
    '''
    \nReturns true if its friday rush hours, false otherwise.
    \nParameter: time when the order was made (UTC in ISO format).
    \ntime format: 2024-01-15T13:00:00Z
    '''
    timestamp = datetime.strptime(order_time, "%Y-%m-%dT%H:%M:%SZ")
    order_hour = timestamp.hour

    if timestamp.isoweekday() != 5: #rush hours only apply during friday
        return False
    
    if 15 <= order_hour and order_hour < 19:
        return True
    
    return False

def extra_distance_fee(distance: int, distance_for_base_fee: int) -> int:
    '''
    Returns the extra distance fee for deliveries that are over "distance_for_base_fee"
    '''
    distance_fee = 0
    for _ in range(distance_for_base_fee, distance, 500): #for every 500m, 1€ is added to distance fee
        distance_fee += 100

    return distance_fee

def extra_items_fee(number_of_items: int, surcharge_item_limit: int ) -> int:
    '''
    \nCalculates the extra fee that comes when ordering more items than "SURCHARGE_ITEM_LIMIT".
    \nAlso adds a bulk fee if the customer orders more items than the item limit for the bulk fee
    '''
    extra_items_fee = 0

    for _ in range(surcharge_item_limit, number_of_items):
        extra_items_fee += 50     #the fee is 50 cents for every item over 4 items

    if number_of_items > 12: #extra "bulk" fee if more than 12 items in cart
        extra_items_fee += 120

    return extra_items_fee


def calculate_delivery_fee(customer_order: dict[str, int | str]) -> int:
    '''
    Takes the JSON request payload as parameter and returns the delivery fee
    '''
    delivery_fee = 0

    cart_value = customer_order["cart_value"]
    delivery_distance = customer_order["delivery_distance"]
    number_of_items = customer_order["number_of_items"]
    order_time = customer_order["time"]

    if cart_value >= LIMIT_FOR_FREE_DELIVERY:  
        return {"delivery_fee": 0}    
    
    if cart_value < MINIMUM_ORDER: #small order surcharge
        delivery_fee = MINIMUM_ORDER - cart_value
    
    delivery_fee += BASE_DELIVERY_FEE

    if delivery_distance > DISTANCE_FOR_BASE_FEE:
        delivery_fee += extra_distance_fee(delivery_distance, DISTANCE_FOR_BASE_FEE)

    if number_of_items > SURCHARGE_ITEM_LIMIT:
        delivery_fee += extra_items_fee(number_of_items, SURCHARGE_ITEM_LIMIT)

    if friday_rush(order_time):
        delivery_fee *= 1.2

    if delivery_fee > MAX_DELIVERY_FEE:  
        return {"delivery_fee": MAX_DELIVERY_FEE}    
    
    return {"delivery_fee": int(delivery_fee)}


app = Flask(__name__)

@app.route("/", methods=['POST'])

def handle_post_requests():
    '''
    \nThis function takes the request payload, validates the received data and returns a response with the calculated delivery fee.
    \nThe function checks if the received data has the right keys and that the keys have the right type of value paired with the given key. 
    \nThe functions raises an Execption and returns an error response if the received data is not JSON or if any key or value of a key is invalid.
    '''
    try:
        data = request.get_json()

        keys_and_types_expected = {"cart_value": int, 
                                   "delivery_distance": int, 
                                   "number_of_items": int, 
                                   "time": str}

        for key in keys_and_types_expected:
            if key not in data:
                raise KeyError(f'Invalid key or {key} not found')
        
        for key in keys_and_types_expected:
            if not isinstance(data[key], keys_and_types_expected[key]):
                raise ValueError('Wrong type paired with a key')

        return jsonify(calculate_delivery_fee(data))
    
    except Exception as e:

        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)