"""
Lab 7: Fuzz Testing with Hypothesis
Property-based test suite for processor.py (Visa Application module).
Tests the explicit compatibility interface exposed by processor.py.
"""

import math
from hypothesis import given, strategies as st
from processor import parse_application, processing_average, payable_fee


# =====================================================================
# 1. NO-CRASH FUZZ TESTS (Handout Starter Requirements)
# =====================================================================

@given(st.text() | st.none())
def test_parse_application_no_crash(s):
    """
    Fuzz test parse_application with arbitrary text or None.
    The function must never crash with unhandled exceptions.
    """
    try:
        res = parse_application(s)
        if res is not None:
            visa_type, entries = res
            assert isinstance(visa_type, str)
            assert len(visa_type) > 0
            assert isinstance(entries, int)
            assert entries > 0
    except Exception as e:
        assert False, f"parse_application crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_processing_average_no_crash(s):
    """
    Fuzz test processing_average with arbitrary text or None.
    The function must never crash with unhandled exceptions.
    """
    try:
        res = processing_average(s)
        if res is not None:
            assert isinstance(res, int)
            assert res >= 0
    except Exception as e:
        assert False, f"processing_average crashed with {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    """
    Fuzz test payable_fee with arbitrary text or None.
    The function must never crash with unhandled exceptions.
    """
    try:
        res = payable_fee(s)
        if res is not None:
            assert isinstance(res, (int, float))
            assert math.isfinite(res)
            assert res >= 0
    except Exception as e:
        assert False, f"payable_fee crashed with {type(e).__name__}: {e}"


# =====================================================================
# 2. VALID INPUT PROPERTY-BASED TESTS
# =====================================================================

@given(
    visa=st.from_regex(r"[a-zA-Z]{2,20}", fullmatch=True),
    entries=st.integers(min_value=1, max_value=50)
)
def test_parse_application_valid_inputs(visa, entries):
    """
    Test parse_application with valid inputs.
    Verifies that formatting, stripping, title-casing, and parsing succeed.
    """
    formatted_input = f"  {visa.lower()}  :  {entries}  "
    result = parse_application(formatted_input)
    assert result is not None, f"Failed on valid input: {formatted_input}"
    visa_res, entries_res = result
    assert visa_res == visa.title()
    assert entries_res == entries


@given(
    days=st.lists(st.integers(min_value=1, max_value=365), min_size=1, max_size=50)
)
def test_processing_average_valid_inputs(days):
    """
    Test processing_average with valid CSV lists of positive integers.
    Verifies that the average matches mathematical expectation sum // len,
    and obeys the bounded property min(days) <= avg <= max(days).
    """
    days_csv = ",".join(str(d) for d in days)
    avg = processing_average(days_csv)
    assert avg is not None, f"Failed on valid CSV: {days_csv}"
    expected = sum(days) // len(days)
    assert avg == expected
    assert min(days) <= avg <= max(days)


@given(
    fee=st.floats(min_value=0.0, max_value=100000.0, allow_nan=False, allow_infinity=False),
    discount=st.floats(min_value=0.0, max_value=100000.0, allow_nan=False, allow_infinity=False)
)
def test_payable_fee_valid_inputs(fee, discount):
    """
    Test payable_fee with valid numeric fee and discount.
    Verifies that total calculation fee * 1.18 - discount is non-negative and accurate.
    """
    text_input = f"{fee:.2f}|{discount:.2f}"
    result = payable_fee(text_input)
    assert result is not None, f"Failed on valid input: {text_input}"
    expected = max(round(float(f"{fee:.2f}") * 1.18 - float(f"{discount:.2f}"), 2), 0.0)
    assert abs(result - expected) < 1e-2
    assert result >= 0.0


# =====================================================================
# 3. EDGE CASES, BOUNDARIES, AND INVALID INPUT TESTS
# =====================================================================

@given(
    invalid_input=st.one_of(
        st.integers(),
        st.booleans(),
        st.lists(st.text()),
        st.sampled_from([
            "",
            "   ",
            "tourist",            # Missing colon delimiter
            "tourist:2:extra",    # Multiple delimiters
            ":2",                 # Missing visa type
            "123:2",              # Non-alphabetic visa type
            "tourist:abc",        # Non-numeric entries
            "tourist:",           # Missing entries
            "tourist:-1",         # Negative entries
            "tourist:0",          # Zero entries
            "tourist:2.5",        # Float instead of integer
        ])
    )
)
def test_parse_application_invalid_inputs(invalid_input):
    """
    Test parse_application against malformed formats, wrong types, and invalid boundaries.
    Must return None safely without raising unexpected exceptions.
    """
    try:
        res = parse_application(invalid_input)
        assert res is None, f"Expected None for invalid input: {invalid_input!r}, got: {res}"
    except Exception as e:
        assert False, f"parse_application crashed with {type(e).__name__}: {e}"


@given(
    invalid_input=st.one_of(
        st.integers(),
        st.booleans(),
        st.lists(st.integers()),
        st.sampled_from([
            "",
            "   ",
            ",",
            "5,,10",              # Empty element in CSV
            ",5,10",              # Leading comma
            "5,10,",              # Trailing comma
            "5,abc,10",           # Non-numeric item
            "-5,10",              # Negative processing days
            "5.5,10",             # Float processing days
        ])
    )
)
def test_processing_average_invalid_inputs(invalid_input):
    """
    Test processing_average against empty strings, bad delimiters, and non-positive numbers.
    Must return None safely without raising unexpected exceptions.
    """
    try:
        res = processing_average(invalid_input)
        assert res is None, f"Expected None for invalid input: {invalid_input!r}, got: {res}"
    except Exception as e:
        assert False, f"processing_average crashed with {type(e).__name__}: {e}"


@given(
    invalid_input=st.one_of(
        st.integers(),
        st.booleans(),
        st.lists(st.floats()),
        st.sampled_from([
            "",
            "   ",
            "|",
            "6000",               # Missing delimiter
            "6000|500|100",       # Multiple delimiters
            "|500",               # Missing fee
            "6000|",              # Missing discount
            "abc|500",            # Non-numeric fee
            "6000|xyz",           # Non-numeric discount
            "-6000|500",          # Negative fee
            "6000|-500",          # Negative discount
            "nan|500",            # NaN fee
            "6000|inf",           # Infinite discount
        ])
    )
)
def test_payable_fee_invalid_inputs(invalid_input):
    """
    Test payable_fee against missing delimiters, non-numeric values, negative numbers, and NaNs.
    Must return None safely without raising unexpected exceptions.
    """
    try:
        res = payable_fee(invalid_input)
        assert res is None, f"Expected None for invalid input: {invalid_input!r}, got: {res}"
    except Exception as e:
        assert False, f"payable_fee crashed with {type(e).__name__}: {e}"


@given(
    fee=st.floats(min_value=10.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
    d1=st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False),
    d2=st.floats(min_value=0.0, max_value=500.0, allow_nan=False, allow_infinity=False)
)
def test_payable_fee_monotonicity(fee, d1, d2):
    """
    Property test: For any positive fee, a larger discount must result in a smaller or equal payable fee.
    """
    smaller_disc = min(d1, d2)
    larger_disc = max(d1, d2)
    res_smaller = payable_fee(f"{fee:.2f}|{smaller_disc:.2f}")
    res_larger = payable_fee(f"{fee:.2f}|{larger_disc:.2f}")
    assert res_smaller is not None and res_larger is not None
    assert res_smaller >= res_larger >= 0.0


# =====================================================================
# 4. OVERFLOW REGRESSION TEST
# =====================================================================

@given(
    fee=st.one_of(
        st.floats(min_value=1.55e308, max_value=1.7976931348623157e+308, allow_nan=False, allow_infinity=False),
        st.sampled_from(["1.6e308", "1.7e308", "1.79e308", "1e309"])
    )
)
def test_payable_fee_rejects_overflow(fee):
    """
    Overflow regression test: Finite inputs that cause calculation overflow
    to infinity (fee * 1.18 -> inf) must be rejected safely (return None)
    without raising unhandled exceptions or returning non-finite values.
    """
    text_input = f"{fee}|0"
    res = payable_fee(text_input)
    assert res is None, f"Expected None on arithmetic overflow for {text_input}, got: {res}"
