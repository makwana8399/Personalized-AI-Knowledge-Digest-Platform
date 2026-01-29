from uuid import uuid4
from datetime import datetime

from app.database.db import SessionLocal, engine
from app.database.models import Base, User, Source


def seed():
    # ✅ Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # -------------------------
        # Create users (if not exists)
        # -------------------------
        users_data = [
            {
                "email": "harshildarji8399@gmail.com",
                "interests": ["LLMs", "MLOps", "Startups"],
            },
            {
                "email": "topgharry8399@gmail.com",
                "interests": ["LLMs", "AI", "MLOps"],
            },
            {
                "email": "harshildarji13@gmail.com",
                "interests": ["Startups", "VC", "Product"],
            },
        ]

        for u in users_data:
            exists = db.query(User).filter(User.email == u["email"]).first()
            if not exists:
                db.add(
                    User(
                        id=uuid4(),
                        email=u["email"],
                        interests=u["interests"],
                        created_at=datetime.utcnow(),
                    )
                )

        # -------------------------
        # Create sources (ONLY BLOG)
        # -------------------------
        sources_data = [
            ("Blog", "blog", 0.9),
            ("YouTube", "youtube", 0.7),
            ("Newsletter", "newsletter", 0.7),
        ]

        for name, type_, score in sources_data:
            exists = db.query(Source).filter(Source.name == name).first()
            if not exists:
                db.add(
                    Source(
                        name=name,
                        type=type_,
                        reliability_score=score,
                    )
                )

        db.commit()
        print("✅ Database seeded successfully")

    except Exception as e:
        db.rollback()
        print("❌ Seeding failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed()