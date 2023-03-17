from Products.models import PropertyValuePairs,ProductProperties
def product_has_property_value_pair(product,properties):
    """
    Parameters:

    product - The product to be checked
    properties - A dictionary of the properties to check.

    Returns True if product has property with the value selected.
    Returns False otherwise
    """
    keys = properties.keys()
    total_properties_to_filter = len(keys)
    count_matches = 0
    for key in keys:
        
        value = properties[key]
        pair  = PropertyValuePairs.objects.get(property__property_name=key,value__value_name=value)
        try:
            product_property_object = ProductProperties.objects.get(product=product,property_value_pair=pair)
            count_matches +=1
        except ProductProperties.DoesNotExist:
            continue
    
    if count_matches == total_properties_to_filter:
        return True
    else:
        return False
