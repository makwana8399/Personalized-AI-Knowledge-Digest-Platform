
from app.database.db import SessionLocal
from app.database.models import User
from app.utils.topics import normalize_interest
from app.config.logging import logger


def main():
    db = SessionLocal()
    users = db.query(User).all()

    updated = 0

    for user in users:
        new_interests = set()

        for interest in user.interests:
            canonical = normalize_interest(interest)
            if canonical:
                new_interests.add(canonical)

        if new_interests and set(user.interests) != new_interests:
            logger.info(
                f"Updating {user.email}: {user.interests} → {list(new_interests)}"
            )
            user.interests = list(new_interests)
            updated += 1

    db.commit()
    db.close()

    logger.info(f"✅ Updated interests for {updated} users")


if __name__ == "__main__":
    main()