"""
log_redaction.py

Redacts credentials from diagnostic messages before logging.
"""

import re


_REDACTED = "[REDACTED]"

# Query parameters that may carry credentials.
_QUERY_SECRET_PATTERN = re.compile(
    r"(?P<prefix>(?:[?&;]|\b)"
    r"(?:api[_-]?key|access[_-]?token|"
    r"auth[_-]?token|token|client[_-]?secret|password)"
    r"\s*=\s*)"
    r"(?P<value>[^&#;\s\"'<>]*)",
    re.IGNORECASE,
)

# Authentication header values.
_AUTH_HEADER_PATTERN = re.compile(
    r"(?P<prefix>\b(?:Authorization|Proxy-Authorization)"
    r"\s*:\s*(?:Bearer|Basic)\s+)"
    r"(?P<value>[^\s,;\"'<>]+)",
    re.IGNORECASE,
)

_API_KEY_HEADER_PATTERN = re.compile(
    r"(?P<prefix>\b(?:X-API-Key|API-Key|ApiKey)"
    r"\s*:\s*)"
    r"(?P<value>[^\s,;\"'<>]+)",
    re.IGNORECASE,
)

_BEARER_PATTERN = re.compile(
    r"(?P<prefix>\bBearer\s+)"
    r"(?P<value>[A-Za-z0-9._~+/=-]+)",
    re.IGNORECASE,
)


def redact_secrets(message, secrets=None):
    """
    Redact common credential formats and explicitly supplied secrets.

    The input is converted to text; the original object is not modified.
    """

    text = str(message)

    text = _QUERY_SECRET_PATTERN.sub(
        lambda match: match.group("prefix") + _REDACTED,
        text,
    )

    text = _AUTH_HEADER_PATTERN.sub(
        lambda match: match.group("prefix") + _REDACTED,
        text,
    )

    text = _API_KEY_HEADER_PATTERN.sub(
        lambda match: match.group("prefix") + _REDACTED,
        text,
    )

    text = _BEARER_PATTERN.sub(
        lambda match: match.group("prefix") + _REDACTED,
        text,
    )

    # Replace explicitly known secrets, longest first.
    known_secrets = sorted(
        (
            str(secret)
            for secret in (secrets or ())
            if secret is not None and str(secret)
        ),
        key=len,
        reverse=True,
    )

    for secret in known_secrets:
        text = text.replace(secret, _REDACTED)

    return text
