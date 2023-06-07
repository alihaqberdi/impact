from datetime import datetime, timedelta


def get_next_day(date_str):
    # Convert the date string to a datetime object
    date = datetime.strptime(date_str, '%d.%m.%Y')

    # Add one day to the date
    next_day = date + timedelta(days=1)

    # Format the next day as a string in the same format

    return next_day