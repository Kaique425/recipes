def is_positive_number(value):
    try:
        float_number = float(value)
    except:
        return False
    return float_number > 0
