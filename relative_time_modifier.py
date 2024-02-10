from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re


def parse(input_str):
    # Extract base date, modifiers, and snapping instructions
    base_date_str, modifiers = input_str.split("()")
    if base_date_str != "now":
        raise ValueError("Base date should be 'now'")

    # Get current UTC date and time
    base_date = datetime.utcnow()

    snap_instructions = {
        "d": dict(hour=0, minute=0, second=0, microsecond=0),
        "h": dict(minute=0, second=0, microsecond=0),
        "m": dict(second=0, microsecond=0),
        "s": dict(microsecond=0),
        "mon": dict(day=1, hour=0, minute=0, second=0, microsecond=0),
        "y": dict(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    }

    # Check for invalid characters(Error Handling)
    invalid_characters = set(modifiers) - set("0123456789+@-dhymon")
    if invalid_characters:
        raise ValueError(
            f"Invalid character(s) detected in modifiers: {invalid_characters}")

    # Check for multiple invalid operators(Error Handling)
    if '-+' in modifiers or '+-' in modifiers:
        raise ValueError(
            "+- or -+ should not be entered in front of identifier")

    # Check for invalid cases where there are no number digits in front of identifiers(Error Handling)
    time_units = {'y': 'year', 'mon': 'month', 'd': 'day',
                  'm': 'minute', 'h': 'hour'}
    for unit in time_units:
        if re.search(fr'[\+\-]{unit}', modifiers) and not re.search(fr'\d+{unit}', modifiers):
            raise ValueError(
                f"Invalid modifier: {time_units[unit]} should have a number digit in front of {unit}")

    pattern = r'(?P<part>[+-]\d+\w+)'

    modifier_list = re.findall(pattern, modifiers)

    # Initialize offset variables
    offset_days = 0
    offset_hours = 0
    offset_minutes = 0
    offset_months = 0
    offset_years = 0

    # Parse each modifier, handling time units/values
    for modifier in modifier_list:
        if not modifier:
            continue
        if "+" in modifier:
            operator = "+"
        else:
            operator = "-"

        value = int("".join(char for char in modifier if char.isdigit()))
        time_units = "".join(char for char in modifier if char.isalpha())
        if time_units == "d":
            offset_days += value * (1 if operator == "+" else -1)
        elif time_units == "h":
            offset_hours += value * (1 if operator == "+" else -1)
        elif time_units == "m":
            offset_minutes += value * (1 if operator == "+" else -1)
        elif time_units == "mon":
            offset_months += value * (1 if operator == "+" else -1)
        elif time_units == "y":
            offset_years += value * (1 if operator == "+" else -1)
        else:
            raise ValueError(f"Invalid time unit: {time_units}")

    # Applying addition/subtraction to the base date
    base_date += timedelta(
        days=offset_days, hours=offset_hours, minutes=offset_minutes
    ) + relativedelta(months=offset_months, years=offset_years)

    # Handle snapping instructions(@d, @mon, @y, @m, @s)
    if "@" in modifiers:
        _, snap_instruction = modifiers.split("@")
        if snap_instruction not in snap_instructions:
            raise ValueError(f"Invalid snap unit: {snap_instruction}")
        base_date = base_date.replace(**snap_instructions[snap_instruction])

    return base_date


# Test cases
print(parse("now()"))

date_strings = [
    # Addition
    "now()+1d@h",
    "now()+2h@m",
    "now()+3mon@d",
    "now()+1y@mon",
    "now()+28d",
    # subtraction
    "now()-1h",
    "now()-1d@h",
    "now()-2h@m",
    "now()-3mon@d",
    "now()-1y@mon",
    # snap only
    "now()@h",
    "now()@m",
    "now()@d",
    "now()@mon",
    "now()@y",
    # combined
    "now()-1y-2mon+3d@h",
    "now()+1mon-15d@h",
    "now()+2y-1mon@mon",
    "now()-3d-12h@h",
]

for dateform in date_strings:
    print(dateform, parse(dateform))
