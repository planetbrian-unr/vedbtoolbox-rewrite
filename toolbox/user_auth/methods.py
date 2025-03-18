from toolbox import db
from toolbox.models import User
from sqlalchemy.exc import SQLAlchemyError

def is_first_user() -> bool:
    # Only the first user is admin by default
    # Allows kickstarting without need to modify SQLite DB directly.
    return User.query.first() is None

def add_user_to_local_db(token):
    try:
        # Parse returned JSON in token for specific attributes
        user_info = token.get("userinfo", {})
        user_id = user_info.get("sub")
        username = user_info.get("nickname")
        email = user_info.get("email")

        # Add/update the user in the database
        user_in_db = User.query.filter_by(user_id=user_id).first()
        if not user_in_db:
            # Add new user if not already in the database
            new_user = User(
                user_id = user_id,
                username = username,
                email = email,
                admin = is_first_user()
            )
            db.session.add(new_user)
            db.session.commit()
            return {"status": "success", "message": "User successfully added to DB."}
        else:
            # Update existing user if necessary
            user_in_db.username = username
            user_in_db.email = email
            db.session.commit()
            return {"status": "success", "message": "User successfully updated with new details."}

    except SQLAlchemyError as e:
        # Handle database-related errors
        db.session.rollback()
        return {"status": "error", "message": "An error occurred while interacting with the database."}

    except Exception as e:
        # Handle other errors
        return {"status": "error", "message": "An unexpected error occurred."}
