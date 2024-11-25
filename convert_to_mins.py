time_strings = [
    "01m 12s",
    "11m 35s",
    "05m 58s",
    "12m 40s",
    "71m 24s",
    "26m 42s",
    "15m 13s",
    "14m 43s",
    "02m 29s",
    "07m 00s",
    "30m 42s"
]

def convert_to_minutes(time_string):
    minutes_str, seconds_str = time_string.split(" ")
    minutes = int(minutes_str[:-1])
    seconds = int(seconds_str[:-1])
    total_minutes = minutes + (seconds / 60)
    return round(total_minutes, 2)

converted_times = [convert_to_minutes(time_string) for time_string in time_strings]
print(converted_times)

