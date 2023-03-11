"""
initital
"""

from yoyo import step

__depends__ = {} # type: ignore

steps = [
    step("""
        CREATE TABLE telegram_user (
            id int PRIMARY KEY,
            name text
        );
    """),
    step("""
        CREATE TABLE exercise (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            type text NOT NULL,
            body json NOT NULL,
            difficulty int
        );
    """)
]
