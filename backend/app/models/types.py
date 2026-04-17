from sqlalchemy import JSON, Text
from sqlalchemy.dialects.postgresql import INET as PG_INET
from sqlalchemy.dialects.postgresql import JSONB as PG_JSONB
from sqlalchemy.types import String, TypeDecorator


class INETType(TypeDecorator):
    """INET for PostgreSQL, String for SQLite and others."""

    impl = String(45)  # 45 chars enough for IPv6 + prefix
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_INET())
        return dialect.type_descriptor(self.impl)


class JSONBType(TypeDecorator):
    """JSONB for PostgreSQL, JSON or TEXT for SQLite and others."""

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_JSONB())
        # SQLite uses JSON (if recent version) or TEXT (fallback)
        # SQLAlchemy handles JSON automatically with sqlite >= 3.9
        return dialect.type_descriptor(JSON())
