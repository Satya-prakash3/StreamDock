import uuid
from beanie import Document
from typing import Optional
from datetime import datetime
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from app.common.utils import (
    utc_now,
)


class CreationMixin(BaseModel):
    """Adds creation metadata (immutable after first save)."""

    created_by: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=utc_now)

    async def ensure_created(self):
        """Set created_at only once if missing."""
        if not self.created_at:
            self.created_at = utc_now()


class UpdationMixin(BaseModel):
    """Adds update metadata (changes every save)."""

    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None

    async def touch(self, user_id: Optional[str] = None):
        """Refresh updated_at (and optionally updated_by)."""
        self.updated_at = utc_now()
        if user_id:
            self.updated_by = user_id


class BaseTimeStampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    async def ensure_created(self):
        """Ensure created_at never changes once set."""
        if not self.created_at:
            self.created_at = datetime.now(utc_now())

    async def touch(self):
        """Refresh updated_at."""
        self.updated_at = datetime.now(utc_now())


class BaseDocument(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    """
    Root base for all Beanie documents.
    Detects and updates timestamp fields automatically.
    """

    async def save(self, user_id: Optional[str] = None, *args, **kwargs):
        """
        Automatically manages created_at and updated_at fields
        if the corresponding attributes exist.
        """

        # --- Handle creation ---
        if hasattr(self, "created_at"):
            created_at = getattr(self, "created_at", None)
            if not created_at:
                setattr(self, "created_at", utc_now())
                if hasattr(self, "created_by") and user_id:
                    setattr(self, "created_by", user_id)

        # --- Handle update ---
        if hasattr(self, "updated_at"):
            setattr(self, "updated_at", utc_now())
            if hasattr(self, "updated_by") and user_id:
                setattr(self, "updated_by", user_id)

        await super().save(*args, **kwargs)

    class Settings:
        pass


class BaseSQLModel(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        String(36),
        default=str(uuid.uuid4()), 
        primary_key=True, 
        unique=True, 
        nullable=False
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class CreationMixinSQL:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    created_by: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
    )


class UpdationMixinSQL:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    updated_by: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
    )


class TimeStampMixinSQL:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
