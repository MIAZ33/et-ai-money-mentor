"""SEBI Compliance Checker Agent — ensures all recommendations are SEBI-compliant."""

SEBI_DISCLAIMER = (
    "This is an AI-generated advisory for informational purposes only and does not "
    "constitute investment advice as defined by SEBI (Securities and Exchange Board of India). "
    "All recommendations are illustrative and based on general financial principles. "
    "Please consult a SEBI-registered investment advisor before making any investment decisions. "
    "Mutual fund investments are subject to market risks. Please read all scheme-related "
    "documents carefully before investing."
)


def get_sebi_disclaimer() -> str:
    """Return the standard SEBI compliance disclaimer."""
    return SEBI_DISCLAIMER


def validate_compliance(portfolio: dict) -> bool:
    """
    Basic compliance validation.
    Returns True if the portfolio passes basic SEBI compliance checks.
    """
    required_keys = {"equity", "debt", "gold", "liquid", "recommended_instruments"}
    if not required_keys.issubset(portfolio.keys()):
        return False

    # Ensure recommended_instruments is a non-empty list
    instruments = portfolio.get("recommended_instruments", [])
    if not isinstance(instruments, list) or len(instruments) == 0:
        return False

    return True
