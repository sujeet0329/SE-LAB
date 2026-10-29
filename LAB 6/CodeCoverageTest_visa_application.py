import pytest
from visa_application import visa_fee, documents_complete, application_status


# Tests for visa_fee - Line Coverage
def test_visa_fee_unknown_type():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("transit", 2, "normal", "B")


def test_visa_fee_negative_entries():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_visa_fee_nationality_group_a_bonus():
    # Group A gets +1 included entry for tourist visa (1 + 1 = 2 included)
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_visa_fee_within_included():
    # Tourist visa includes 1 entry; 1 entry used -> extra <= 0
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_visa_fee_express_speed_standard_extra():
    # Tourist: 1 included. 3 entries -> extra = 2 (<= 5). Express rate = 100.
    # Total = 2 * 100 = 200
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_visa_fee_normal_speed_extra_over_five():
    # Tourist: 1 included. 7 entries -> extra = 6 (> 5). Normal rate = 40 + 20 = 60.
    # Total = 6 * 60 = 360
    assert visa_fee("tourist", 7, "normal", "B") == 360


def test_visa_fee_express_speed_extra_over_five():
    # Business: 3 included. 10 entries -> extra = 7 (> 5). Express rate = 100 + 20 + 10 = 130.
    # Total = 7 * 130 = 910
    assert visa_fee("business", 10, "express", "B") == 910


# Tests for documents_complete - Line Coverage
def test_documents_complete_renewal_valid():
    assert documents_complete(1, 0, True) is True


def test_documents_complete_renewal_invalid():
    assert documents_complete(0, 0, True) is False


def test_documents_complete_insufficient_photos():
    assert documents_complete(3, 1, False) is False


def test_documents_complete_standard_valid():
    assert documents_complete(3, 2, False) is True


def test_documents_complete_standard_invalid_forms():
    assert documents_complete(2, 2, False) is False


# Tests for application_status - Line Coverage
def test_application_status_express_peak_open():
    # Express (10) + Peak (15) = cutoff 25; days_left = 25 -> open
    assert application_status(25, True, True) == "open"


def test_application_status_standard_closing():
    # Normal (30) + Non-peak (0) = cutoff 30; cutoff - 15 = 15; days_left = 20 -> closing
    assert application_status(20, False, False) == "closing"


def test_application_status_closed():
    # Normal (30) + Non-peak (0) = cutoff 30; cutoff - 15 = 15; days_left = 10 -> closed
    assert application_status(10, False, False) == "closed"
