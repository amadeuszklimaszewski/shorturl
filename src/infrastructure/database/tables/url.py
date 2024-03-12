from sqlalchemy import Column, String, Table
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.database.metadata import metadata

url_table = Table(
    "group",
    metadata,
    Column("short_url", UUID(as_uuid=True), primary_key=True),
    Column("original_url", String(), nullable=False),
)
