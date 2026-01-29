from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

from app.config.settings import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Create tables + seed default sources
    """
    from app.database.models import Source  # lazy import

    print("📦 Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        default_sources = [
            {
                "name": "Blog",
                "type": "rss",
            },
            {
                "name": "YouTube",
                "type": "video",
            },
            {
                "name": "Newsletter",
                "type": "email",
            },
        ]

        for src in default_sources:
            exists = (
                db.query(Source)
                .filter(Source.name == src["name"])
                .first()
            )

            if not exists:
                db.add(
                    Source(
                        name=src["name"],
                        type=src["type"],
                        reliability_score=1.0,
                        created_at=datetime.utcnow(),
                    )
                )
                print(f"✅ Inserted source: {src['name']}")

        db.commit()
        print("🎯 Database initialized successfully")

    except Exception as e:
        db.rollback()
        print("❌ DB init failed:", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()