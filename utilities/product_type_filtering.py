
def count_fields_values(model, field, text):
    # Stuff

    filters = {
        field+'__icontains': text
    }
    total = len(model.objects.filter(**filters))
    
    return total