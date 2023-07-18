import datetime
import uuid
from db.schema import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'users'

    id: so.Mapped[uuid.UUID] = so.mapped_column(sa.UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(), nullable=False, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(), nullable=False)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(), nullable=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(), nullable=True)

    admin: so.Mapped[str] = so.mapped_column(sa.Boolean(), nullable=False, default=False)

    created_at: so.Mapped[datetime.datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    active: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False)
