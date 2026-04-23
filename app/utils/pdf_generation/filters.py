def comma_format(value):
    """Format a number with commas as thousands separators.

    Args:
        value (int or float): The number to format.

    Returns:
        str: The formatted number as a string with commas.
    """
    try:
        return "{:,}".format(int(value))
    except (ValueError, TypeError):
        return value
