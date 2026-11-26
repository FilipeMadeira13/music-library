import secrets

import pytest


@pytest.fixture
def password() -> str:
    """Return a random per-test password, so no credential-like literal is committed."""
    return secrets.token_urlsafe(16)


@pytest.fixture
def other_password(password: str) -> str:
    """Return a second random password, guaranteed to differ from ``password``."""
    while (value := secrets.token_urlsafe(16)) == password:
        continue
    return value
