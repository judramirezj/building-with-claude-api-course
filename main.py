def greeting():
    print("Hi there")


def calculate_pi(digits=5):
    """
    Calculate pi to a specified number of decimal digits using the Machin formula.
    Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    
    Args:
        digits: Number of decimal places to calculate (default: 5)
    
    Returns:
        float: Approximation of pi
    """
    from decimal import Decimal, getcontext
    
    # Set precision higher than needed for accuracy
    getcontext().prec = digits + 10
    
    def arctan(x, num_terms=100):
        """Calculate arctan using Taylor series expansion"""
        x = Decimal(x)
        power = x
        result = power
        for n in range(1, num_terms):
            power *= -x * x
            result += power / (2 * n + 1)
        return result
    
    # Machin's formula
    pi = 4 * (4 * arctan(Decimal(1) / Decimal(5)) - arctan(Decimal(1) / Decimal(239)))
    
    return float(pi)


def calculate_pi_simple():
    """
    Calculate pi to the 5th decimal digit (3.14159) using the Machin formula.
    
    Returns:
        float: Pi approximated to 5 decimal places
    """
    return round(calculate_pi(5), 5)