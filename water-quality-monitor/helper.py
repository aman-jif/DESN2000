# Simple helper function to add truncation without rounding
def decimal_trunc(float, power):
    mult = 10 ** power
    return int(float * mult) / mult