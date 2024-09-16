import json

def calculate_total_travel_time(data):
    # Calculate total travel time
    total_duration = sum(leg['duration']['value'] for leg in data['routes'][0]['legs'])

    # Convert the total duration from seconds to hours, minutes, and seconds
    hours, remainder = divmod(total_duration, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Return the formatted total travel time
    if hours > 0:
        return f"Total travel time: {hours} hours, {minutes} minutes, {seconds} seconds"
    else:
        return f"Total travel time: {minutes} minutes, {seconds} seconds"
