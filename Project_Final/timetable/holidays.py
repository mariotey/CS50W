from datetime import datetime

def add_update_holidays():
    current_datetime = datetime.now()

    # If current date is a Monday,
    if current_datetime.weekday() == 0:
        print("Current date is a Monday.")



    else:
        print("Current date is not a Monday.")