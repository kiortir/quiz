"""
Add username to user
"""

from yoyo import step

__depends__ = {'20230219_03_2tw3C-draft-table'}

steps = [
    step("""
        ALTER TABLE telegram_user
            ADD COLUMN username text;
    """)
]
