"""
draft_table
"""

from yoyo import step

__depends__ = {'20230219_02_fg5Vn-user-exercise'}

steps = [
    step("""
        CREATE TABLE draft (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            type text,
            body json,
            difficulty int,
            user_id int NOT NULL UNIQUE,
            CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES telegram_user(id)
        );
    """),
    step("""
        ALTER TABLE telegram_user
            ADD COLUMN context json;
    """)
]
