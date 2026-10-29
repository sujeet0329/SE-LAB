import pytest
from visa_application import visa_fee, documents_complete, application_status


# ============================================================================
# Branch Coverage Tests for visa_fee
# ============================================================================

def test_visa_fee_unknown_visa_type_branch():
    """Branch: visa_type not in INCLUDED_ENTRIES (True)."""
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("transit", 2, "normal", "B")


def test_visa_fee_negative_entries_branch():
    """Branch: entries < 0 (True)."""
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_visa_fee_zero_entries_boundary():
    """Branch: entries >= 0 (False for entries < 0) and extra <= 0 (True)."""
    # tourist included = 1; entries = 0 -> extra = -1 <= 0 -> return 0
    assert visa_fee("tourist", 0, "normal", "B") == 0


def test_visa_fee_group_a_non_student_branch():
    """
    Branch: nationality_group == 'A' and visa_type != 'student' (True).
    Included entries incremented by 1.
    """
    # Business included = 3. Group A -> included = 4.
    # entries = 4 -> extra = 0 <= 0 -> fee = 0
    assert visa_fee("business", 4, "normal", "A") == 0


def test_visa_fee_group_a_student_branch():
    """
    Branch: nationality_group == 'A' is True BUT visa_type != 'student' is False.
    Student included stays at 2 (not incremented).
    """
    # Student included = 2. entries = 2 -> extra = 0 <= 0 -> fee = 0
    assert visa_fee("student", 2, "normal", "A") == 0


def test_visa_fee_group_b_short_circuit_branch():
    """
    Branch: nationality_group == 'A' is False.
    Included entries not incremented.
    """
    # Tourist included = 1. entries = 1 -> extra = 0 <= 0 -> fee = 0
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_visa_fee_normal_speed_extra_exactly_five_boundary():
    """
    Branches:
    - extra <= 0 (False)
    - speed == 'express' (False -> rate = 40)
    - extra > 5 (False -> boundary extra == 5)
    """
    # Tourist included = 1. entries = 6 -> extra = 5.
    # rate = 40. fee = 5 * 40 = 200
    assert visa_fee("tourist", 6, "normal", "B") == 200


def test_visa_fee_express_speed_extra_exactly_five_boundary():
    """
    Branches:
    - speed == 'express' (True -> rate = 100)
    - extra > 5 (False -> boundary extra == 5)
    """
    # Tourist included = 1. entries = 6 -> extra = 5.
    # rate = 100. fee = 5 * 100 = 500
    assert visa_fee("tourist", 6, "express", "B") == 500


def test_visa_fee_normal_speed_extra_greater_than_five_boundary():
    """
    Branches:
    - speed == 'express' (False -> rate = 40)
    - extra > 5 (True -> boundary extra == 6, rate becomes 60)
    - nested speed == 'express' (False)
    """
    # Tourist included = 1. entries = 7 -> extra = 6.
    # rate = 40 + 20 = 60. fee = 6 * 60 = 360
    assert visa_fee("tourist", 7, "normal", "B") == 360


def test_visa_fee_express_speed_extra_greater_than_five_boundary():
    """
    Branches:
    - speed == 'express' (True -> rate = 100)
    - extra > 5 (True -> boundary extra == 6, rate += 20)
    - nested speed == 'express' (True -> rate += 10 => total rate 130)
    """
    # Tourist included = 1. entries = 7 -> extra = 6.
    # rate = 100 + 20 + 10 = 130. fee = 6 * 130 = 780
    assert visa_fee("tourist", 7, "express", "B") == 780


# ============================================================================
# Branch Coverage Tests for documents_complete
# ============================================================================

def test_documents_complete_renewal_true_forms_valid():
    """Branch: is_renewal is True, forms_filed >= 1 (True)."""
    assert documents_complete(1, 0, True) is True


def test_documents_complete_renewal_true_forms_invalid():
    """Branch: is_renewal is True, forms_filed >= 1 (False)."""
    assert documents_complete(0, 5, True) is False


def test_documents_complete_non_renewal_photos_insufficient_boundary():
    """Branch: is_renewal is False, photos < 2 (True with boundary photos=1)."""
    assert documents_complete(5, 1, False) is False


def test_documents_complete_non_renewal_photos_zero():
    """Branch: is_renewal is False, photos < 2 (True with photos=0)."""
    assert documents_complete(5, 0, False) is False


def test_documents_complete_non_renewal_photos_sufficient_forms_invalid():
    """
    Branches:
    - is_renewal is False
    - photos < 2 (False with boundary photos=2)
    - forms_filed >= 3 (False with boundary forms_filed=2)
    """
    assert documents_complete(2, 2, False) is False


def test_documents_complete_non_renewal_photos_sufficient_forms_valid_boundary():
    """
    Branches:
    - is_renewal is False
    - photos < 2 (False with boundary photos=2)
    - forms_filed >= 3 (True with boundary forms_filed=3)
    """
    assert documents_complete(3, 2, False) is True


def test_documents_complete_non_renewal_photos_sufficient_forms_exceeded():
    """Branch: forms_filed >= 3 (True with forms_filed > 3)."""
    assert documents_complete(4, 3, False) is True


# ============================================================================
# Branch Coverage Tests for application_status
# ============================================================================

def test_application_status_express_non_peak_open_boundary():
    """
    Cutoff = 10.
    Branches: is_express True, is_peak_season False, days_left >= cutoff (True at boundary 10).
    """
    assert application_status(10, True, False) == "open"


def test_application_status_express_non_peak_closing_upper_boundary():
    """
    Cutoff = 10, closing threshold = -5.
    Branches: days_left >= cutoff (False at 9), elif days_left >= -5 (True at 9).
    """
    assert application_status(9, True, False) == "closing"


def test_application_status_express_non_peak_closing_lower_boundary():
    """
    Cutoff = 10, closing threshold = -5.
    Branches: days_left >= cutoff (False), elif days_left >= -5 (True at boundary -5).
    """
    assert application_status(-5, True, False) == "closing"


def test_application_status_express_non_peak_closed_boundary():
    """
    Cutoff = 10, closing threshold = -5.
    Branches: days_left >= cutoff (False), elif days_left >= -5 (False at boundary -6).
    """
    assert application_status(-6, True, False) == "closed"


def test_application_status_express_peak_open():
    """
    Cutoff = 10 + 15 = 25.
    Branches: is_express True, is_peak_season True, days_left >= cutoff (True).
    """
    assert application_status(25, True, True) == "open"


def test_application_status_express_peak_closed():
    """
    Cutoff = 25, closing threshold = 10.
    Branches: days_left >= cutoff (False), elif days_left >= 10 (False at 9).
    """
    assert application_status(9, True, True) == "closed"


def test_application_status_standard_non_peak_open_greater():
    """
    Cutoff = 30.
    Branches: is_express False, is_peak_season False, days_left >= 30 (True at 35).
    """
    assert application_status(35, False, False) == "open"


def test_application_status_standard_non_peak_open_boundary():
    """
    Cutoff = 30.
    Branches: is_express False, is_peak_season False, days_left >= 30 (True at boundary 30).
    """
    assert application_status(30, False, False) == "open"


def test_application_status_standard_non_peak_closing_upper_boundary():
    """
    Cutoff = 30, closing threshold = 15.
    Branches: days_left >= 30 (False at 29), elif days_left >= 15 (True at 29).
    """
    assert application_status(29, False, False) == "closing"


def test_application_status_standard_non_peak_closing_lower_boundary():
    """
    Cutoff = 30, closing threshold = 15.
    Branches: days_left >= 30 (False at 15), elif days_left >= 15 (True at boundary 15).
    """
    assert application_status(15, False, False) == "closing"


def test_application_status_standard_non_peak_closed_boundary():
    """
    Cutoff = 30, closing threshold = 15.
    Branches: days_left >= 30 (False at 14), elif days_left >= 15 (False at boundary 14).
    """
    assert application_status(14, False, False) == "closed"


def test_application_status_standard_peak_open_boundary():
    """
    Cutoff = 30 + 15 = 45.
    Branches: is_express False, is_peak_season True, days_left >= 45 (True at boundary 45).
    """
    assert application_status(45, False, True) == "open"


def test_application_status_standard_peak_closing_boundary():
    """
    Cutoff = 45, closing threshold = 30.
    Branches: days_left >= 45 (False at 44), elif days_left >= 30 (True at 44).
    """
    assert application_status(44, False, True) == "closing"


def test_application_status_standard_peak_closed_boundary():
    """
    Cutoff = 45, closing threshold = 30.
    Branches: days_left >= 45 (False at 29), elif days_left >= 30 (False at boundary 29).
    """
    assert application_status(29, False, True) == "closed"
