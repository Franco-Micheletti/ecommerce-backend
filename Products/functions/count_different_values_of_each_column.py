def count_different_values_of_each_column(response_data,products,product_type_fields_list):

    for column in product_type_fields_list:
        values = products.values(column)
        for value in values:
            try:
                response_data["filters"][column][value[column]] += 1
            except:
                response_data["filters"][column][value[column]] = 1
    
    return response_data