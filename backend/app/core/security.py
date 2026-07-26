from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a password using Argon2 via pwdlib."""
    return password_hash.hash(password)


def get_password_hash(password: str) -> str:
    """Alias for hash_password for backwards compatibility."""
    return hash_password(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify a plain password against a hashed password."""
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def validate_password_strength(password: str) -> bool:
    """Validate that a password meets minimum security requirements (at least 8 characters)."""
    return len(password) >= 8
