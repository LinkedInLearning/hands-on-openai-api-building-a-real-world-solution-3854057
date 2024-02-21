from datetime import date, timedelta

def get_school_week_bounds(input_date: date):
    weekday = input_date.weekday()
    start_of_week = input_date - timedelta(days=weekday)
    end_of_week = start_of_week + timedelta(days=4)
    return start_of_week, end_of_week