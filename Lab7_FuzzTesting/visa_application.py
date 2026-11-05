"""
Visa Application Processing Module
Defensive implementation hardened against invalid, unexpected, boundary,
and arithmetic overflow inputs.
"""

import math


def parse_application(text):
    """
    Parses a visa application string in the format 'visa_type:entries'.

    Args:
        text (str): Input string, e.g., 'tourist:2'.

    Returns:
        tuple (str, int) or None: (Title-cased visa type, positive integer entries)
                                  or None if input is invalid.
    """
    if not isinstance(text, str):
        return None

    if ":" not in text:
        return None

    parts = text.split(":")
    if len(parts) != 2:
        return None

    visa_raw, entries_raw = parts
    visa = visa_raw.strip()
    if not visa:
        return None

    # Ensure visa type consists of alphabetic words (handles single and multi-word names)
    cleaned_name = visa.replace(" ", "")
    if not cleaned_name.isalpha():
        return None

    entries_raw = entries_raw.strip()
    try:
        entries = int(entries_raw)
        if entries <= 0:
            return None
    except (ValueError, TypeError):
        return None

    return visa.title(), entries


def processing_average(days_csv):
    """
    Computes the floor average processing days from a comma-separated string of integers.

    Args:
        days_csv (str): Input string of CSV integers, e.g., '5,10,21'.

    Returns:
        int or None: Floor average processing days, or None if input is invalid.
    """
    if not isinstance(days_csv, str):
        return None

    days_csv = days_csv.strip()
    if not days_csv:
        return None

    tokens = days_csv.split(",")
    if not tokens:
        return None

    values = []
    for token in tokens:
        t = token.strip()
        if not t:
            return None  # Rejects empty tokens like '5,,10' or leading/trailing commas
        try:
            val = int(t)
            if val < 0:
                return None  # Processing days cannot be negative
            values.append(val)
        except (ValueError, TypeError):
            return None

    if not values:
        return None

    return sum(values) // len(values)


def payable_fee(text):
    """
    Computes payable visa fee with 18% tax minus discount: max(fee * 1.18 - discount, 0).
    Guards strictly against non-finite values and intermediate arithmetic overflow.

    Args:
        text (str): Input string in format 'fee|discount', e.g., '6000|500'.

    Returns:
        float or None: Calculated non-negative finite fee, or None if input is invalid
                       or calculation overflows.
    """
    if not isinstance(text, str):
        return None

    if "|" not in text:
        return None

    parts = text.split("|")
    if len(parts) != 2:
        return None

    fee_str, discount_str = parts[0].strip(), parts[1].strip()
    if not fee_str or not discount_str:
        return None

    try:
        fee = float(fee_str)
        discount = float(discount_str)
    except (ValueError, TypeError):
        return None

    # Handle NaN and Inf inputs upfront
    if not math.isfinite(fee) or not math.isfinite(discount):
        return None

    # Fees and discounts cannot be negative
    if fee < 0 or discount < 0:
        return None

    try:
        raw_total = fee * 1.18 - discount
    except OverflowError:
        return None

    # Intermediate calculation must be finite (guards against multiplication overflow)
    if not math.isfinite(raw_total):
        return None

    try:
        total = round(raw_total, 2)
    except OverflowError:
        return None

    if not math.isfinite(total):
        return None

    return max(total, 0.0)


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:", result)

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
