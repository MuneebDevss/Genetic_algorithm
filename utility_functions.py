import re

def is_valid_date(date_str):
    """
    Validates a date string in DD/MM/YYYY format.
    Returns True if valid, False otherwise.
    """

    # Check format (DD/MM/YYYY)
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", date_str):
        return False

    day_str, month_str, year_str = date_str.split("/")

    try:
        day = int(day_str)
        month = int(month_str)
        year = int(year_str)
    except ValueError:
        return False  # Non-integer values

    # Validate year range
    if year < 0 or year > 9999:
        return False

    # Validate month
    if month < 1 or month > 12:
        return False

    # Validate day
    if day < 1:
        return False

    # Days per month logic
    if month in [4, 6, 9, 11] and day > 30:
        return False  # 30-day months
    elif month == 2:
        # Leap year check
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_day = 29 if is_leap else 28
        if day > max_day:
            return False
    elif day > 31:
        return False  # 31-day months

    return True