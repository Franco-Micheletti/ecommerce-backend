from Products.models import ProductProperties


def count_property_values_results(product_name):
    """
    Returns a dictionary of the sum of each existing property value.
    """
    response_data = {
                "filters":{
                    "price":{
                        "max_price":0
                    }
                }
              }
    
    product_properties = ProductProperties.objects.filter(product__product_name__icontains=str(product_name))[0:1000]
    if product_properties:
        for object in product_properties:
            name = object.property_value_pair.property.property_name
            value = object.property_value_pair.value.value_name
            try:
                response_data["filters"][name][value] += 1
            except:
                if name in response_data["filters"]:
                    response_data["filters"][name][value] = 1
                else:
                    response_data["filters"][name] = {}
                    response_data["filters"][name][value] = 1
    return response_data