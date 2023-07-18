from db.schema import Base
import sqlalchemy as sa
import sqlalchemy.orm as so


class EmailSubscriber(Base):
    __tablename__ = 'email_subscriber'

    secret: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)


class EmailPasswordRefresh(Base):
    __tablename__ = 'email_password_refresh'
    secret: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)
