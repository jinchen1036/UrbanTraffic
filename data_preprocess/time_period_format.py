#Build a function to separate the time period for pre, during and post Covid-19
def covid__period(x):
    if (x.year >= 2020) & (x.month >= 3):
        return "In Covid"
    else:
        return "Pre-Covid"

# Build a function to separate by pick up time period
def pick_up_time_period(x):
    if (x.hour >= 0) & (x.hour <= 1):
        return "mid-night rush hours"
    elif (x.hour >= 6) & (x.hour <= 10):
        return "morning rush hours"
    elif (x.hour >= 17) & (x.hour <= 20):
        return "evening rush hours"
    else:
        return "off-peak hours"

# Build a function to parse weekdays or weekend
def weekday_or_weekend(x):
    weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    day_of_the_week = x.weekday()
    day_of_the_week_as_string = weekDays[day_of_the_week]
    if (day_of_the_week_as_string == "Saturday") | (day_of_the_week_as_string == "Sunday"):
        return "Weekend"
    else:
        return "Weekday"
