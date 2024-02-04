import delivery_fee_API as API
'''
Unit tests for delivery_fee_API.py

Run with command `pytest`

'''


def test_small_order_surcharge_1():
    # the example that was given in the assignment
    order =  {"cart_value": 790,
                "delivery_distance": 2235,
                "number_of_items": 4, 
                "time": "2024-01-15T13:00:00Z"
                }
    test = API.calculate_delivery_fee(order)
    assert test == {"delivery_fee": 710}


def test_small_order_surcharge_2():
    # ordering 1 item on a weekday that is not friday and under 1km distance
    # small order surcharge 4.8€ + base delivery 2€ = 6.8€
    order =  {"cart_value": 520,
                 "delivery_distance": 563,
                "number_of_items": 1, 
                "time": "2024-01-16T18:00:00Z" #rush hour but not friday, delivery fee should not be affected
                }
    test = API.calculate_delivery_fee(order)
    assert test == {"delivery_fee": 680}


def test_item_surcharge_1():
    # distance 7e + items and bulk surcharge 6,20e
    order =  {"cart_value": 1000,
                 "delivery_distance": 3320,
                "number_of_items": 14, 
                "time": "2024-01-12T20:02:32Z"
                }
    test = API.calculate_delivery_fee(order)
    assert test == {"delivery_fee": 1320}


def test_item_surcharge_2():
    # 12 items should not give bulk surcharge -> 4e for items, 2e for delivery = 6e
    order =  {"cart_value": 1050,
                 "delivery_distance": 970,
                "number_of_items": 12, 
                "time": "2024-01-16T17:40:43Z"
                }
    test = API.calculate_delivery_fee(order)
    assert test == {"delivery_fee": 600}


def test_free_delivery_1():
    # order value is over 200€, so the delivery should be free
    order =  {"cart_value": 20_200,
                 "delivery_distance": 2235,
                "number_of_items": 2, 
                "time": "2024-01-12T23:00:00Z"
                }
    test = API.calculate_delivery_fee(order)
    assert test == {"delivery_fee": 0}


def test_free_delivery_2():
    # the order value is 200€, so the delivery should be free
    order =  {"cart_value": 20_000,
                 "delivery_distance": 5201,
                "number_of_items": 13, 
                "time": "2024-01-19T17:34:32Z" #rush hour
                }
    test = API.calculate_delivery_fee(order)
    assert test == {"delivery_fee": 0}


def test_friday_not_rush_hour(): 
    #date is friday but its not rush hour
    order =  {"cart_value": 790,
                 "delivery_distance": 2235,
                "number_of_items": 4, 
                "time": "2024-01-19T03:16:54Z"
                }
    test = API.calculate_delivery_fee(order)
    assert test == {"delivery_fee": 710}


def test_friday_rush_hour():
    #it is friday and rush hour, 2.10€ for small delivery surcharge,
    # 5€ for distance -> 7.10€ delivery * 1.2 rush hour fee -> delivery is 8.52€
    order =  {"cart_value": 790,
                 "delivery_distance": 2235,
                "number_of_items": 3, 
                "time": "2024-01-19T18:34:55Z"
                }
    test = API.calculate_delivery_fee(order)
    assert test == {"delivery_fee": 852}


def test_max_delivery():
    #the delivery is over 15€ (15,84€) so the return value should be 15€
    order =  {"cart_value": 1230,
                 "delivery_distance": 3150,
                "number_of_items": 14, 
                "time": "2024-01-19T18:21:12Z" #rush hour 
                }
    test = API.calculate_delivery_fee(order)
    assert test == {"delivery_fee": 1500}