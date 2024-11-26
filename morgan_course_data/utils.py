def format_days(days_array):
    """
    Convert days array to a human-readable string.
    """
    day_map = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
    return ", ".join([day_map.get(day, "Unknown") for day in days_array])
