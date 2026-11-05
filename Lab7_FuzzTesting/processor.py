"""
Lab 7 Compatibility Module: processor.py
=========================================
This module serves as an explicit compatibility wrapper and entrypoint for the
generic Lab 7 submission specification.

Architecture & Domain Mapping:
- Canonical Domain Module: `visa_application.py`
  (Assigned Repository: SETAPESU26/L6_L7_52_visa_application).
- Single Source of Truth (SSOT): All core parsing, calculation, input validation,
  and arithmetic overflow protection logic resides in `visa_application.py`.
- This module explicitly imports and re-exports all three hardened functions
  (`parse_application`, `processing_average`, `payable_fee`) and the interactive `main()`
  CLI runner to ensure 100% compatibility with the generic Lab 7 submission specifications
  without duplicate code or architectural divergence.
"""

from visa_application import (
    parse_application,
    processing_average,
    payable_fee,
    main,
)

__all__ = [
    "parse_application",
    "processing_average",
    "payable_fee",
    "main",
]

if __name__ == "__main__":
    main()
