from sqlalchemy import (
    Column,
    String,
    DateTime,
    ARRAY,
    Integer,
    Float,
    Text,
    Date,
    ForeignKey,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .db import Base
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    interests = Column(ARRAY(String), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    digests = relationship("Digest", back_populates="user")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'blog', 'youtube', 'newsletter'
    reliability_score = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    articles = relationship("Article", back_populates="source")


class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False, index=True)
    content_md = Column(Text)
    summary = Column(Text)
    takeaways = Column(ARRAY(String))
    topic = Column(String, index=True)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    source = relationship("Source", back_populates="articles")


class Digest(Base):
    __tablename__ = "digests"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    generated_date = Column(Date, nullable=False)
    overview = Column(Text)
    article_ids = Column(ARRAY(UUID(as_uuid=True)))

    email_sent = Column(Boolean, default=False)

    user = relationship("User", back_populates="digests")