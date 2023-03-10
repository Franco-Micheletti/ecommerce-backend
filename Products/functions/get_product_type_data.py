from utilities.product_type_classes import product_types

def get_product_type_data(sample):

    response_data = {
                    "filters":{
                        "product_type":"",
                        "price":{
                            "max_price":0
                        }
                    }
                    }
    
    # Count number of each product type for better searching
    # Then query the corresponding product type table

    product_type_ids = {}
    product_type_fields_list = []
    
    for product in sample:
        try:
            product_type_ids[product.product_type_id] += 1
        except:
            product_type_ids[product.product_type_id] = 1
    
    # Get the most popular product type from dictionary
    most_popular_product_type = max(product_type_ids,key=product_type_ids.get)
    
    # Add the product_type to the JSON data

    response_data["filters"]["product_type"] = most_popular_product_type

    # Create list of product types
    for field in product_types[most_popular_product_type][0]._meta.get_fields()[3:]:
        
        product_type_fields_list.append(field.name)

    # Add each property ( a column in DB table ) to the filters key in response_data
    for column in product_type_fields_list:
        
        column = column
        response_data["filters"][column] = {}
    
    return (response_data,most_popular_product_type,product_type_fields_list)