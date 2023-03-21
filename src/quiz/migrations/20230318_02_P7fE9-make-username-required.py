"""
make username required
"""

from yoyo import step

__depends__ = {"20230318_01_pD3fU-add-username-to-user"}

steps = [
    step(
    """
        TRUNCATE TABLE telegram_user CASCADE;   
    """
    ),
    step(
    """
        ALTER TABLE telegram_user
            ALTER COLUMN username SET NOT NULL;
    """
    ),
]
