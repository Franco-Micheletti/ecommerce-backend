from Products.functions.product_has_property_value_pair import product_has_property_value_pair
import json

def filter_products(filters,products):
    """
    Returns a list with all the products that matched the applied filter.
    """
    filters_json = json.loads(filters)
    products_list = []
    
    # FEATURES FILTER 
    if "properties" in filters_json:
        for product in products:
            check = product_has_property_value_pair(product,filters_json["properties"])
            if check:
                products_list.append(product)
            else:
                continue
    else:
        products_list = products
    # PRICE FILTER
    if "price" in filters_json:
        min_price = filters_json["price"]["min"]
        max_price = filters_json["price"]["max"]
        
        def price_range_check(product):
            if product.price >= float(min_price) and product.price <= float(max_price):
                return True
            else:
                return False
        
        products_list = list(filter(price_range_check,products_list))

    return products_list