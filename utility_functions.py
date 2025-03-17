import re
def get_date_category_with_explanation(day, month, year,isValid):
    categories = []
    if isValid:
        if day == 29:
            categories.append("Valid (Leap year)")

        if month in [1, 3, 5, 7, 8, 10, 12]:
            categories.append("Valid (30 days Month)")
        elif month in [4, 6, 9, 11]:
            categories.append("Valid (31 days month)")
        elif month == 2:
            categories.append("Valid (28 days month)")
        
    else:
        if day>31:
             categories.append("Invalid days")
        if month > 12:
            categories.append("Invalid month")
        if year>9999:
            categories.append("Invalid year")
    
    
    if (day == 30 and month in [1, 3, 5, 7, 8, 10, 12]) or (day == 31 and month in [4, 6, 9, 11]) or ((day == 29 and month == 2)):
            categories.append("Boundary Case")
    if year==0000 and month==1 and day==1:
        categories.append("Boundry Case (Minimum)")
    if year == 0 and month == 1 and day == 1:
        categories.append("Boundry Case (Maximum)")
    return categories
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