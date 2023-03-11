"""
user_exercise
"""

from yoyo import step

__depends__ = {"20230219_01_uKxaq-initital"}

steps = [
    step(
        """
        CREATE TABLE user_exercise (
        telegram_user_id int REFERENCES telegram_user(id) ON UPDATE CASCADE ON DELETE CASCADE,
        exercise_id uuid REFERENCES exercise(id) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT user_exercise_pkey PRIMARY KEY (telegram_user_id, exercise_id)
    );
    """
    )
]
