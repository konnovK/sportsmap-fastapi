import smtplib
import uuid
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import md5

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.model.email import EmailPasswordRefresh, EmailSubscriber

from service.exc import EmailPasswordRefreshAlreadyExistsException, EmailPasswordRefreshNotFoundException, \
    EmailSubscriberAlreadyExistsException, EmailSubscriberNotFoundException
from service.model.email_model import EmailPasswordRefreshServiceModel, EmailSubscriberRefreshServiceModel

from settings import Settings


class EmailService:
    class Email:
        def __init__(self):
            self.settings = None
            self.email_user = None
            self.email_password = None
            self.email_host = None
            self.body = None
            self.subject = None
            self.email_to = None

        def set_settings(self, settings: Settings):
            self.settings = settings
            self.email_user = settings.SMTP_USER
            self.email_password = settings.SMTP_PASSWORD
            self.email_host = settings.SMTP_HOST
            return self

        def set_body(self, body: str):
            self.body = body
            return self

        def set_subject(self, subject: str):
            self.subject = subject
            return self

        def set_email_to(self, email_to: str):
            self.email_to = email_to
            return self

        def _email_message(self, email_to: str, subject: str, body: str) -> MIMEMultipart:
            msg = MIMEMultipart('alternative')
            msg.set_charset('utf8')
            msg['FROM'] = self.email_user
            msg['Subject'] = Header(subject, 'utf8')
            msg['To'] = email_to
            _attach = MIMEText(body, _charset='utf8')
            msg.attach(_attach)
            return msg

        def send(self):
            """
            returns `True` if mail was sent, `False` otherwise.
            :param email_to:
            :param subject:
            :param body:
            :return:
            """
            try:
                server = smtplib.SMTP_SSL(self.email_host)
                server.login(self.email_user, self.email_password)
                server.sendmail(
                    self.email_user,
                    self.email_to,
                    self._email_message(
                        self.email_to,
                        self.subject,
                        self.body
                    ).as_string()
                )
                server.quit()
                return True
            except smtplib.SMTPException or ValueError:
                return False

    def __init__(self, async_session, settings: Settings):
        self.async_session = async_session
        self.settings = settings
        self.email_user = settings.SMTP_USER
        self.email_password = settings.SMTP_PASSWORD
        self.email_host = settings.SMTP_HOST

    def _send_mail(self, email_to: str, subject: str, body: str) -> bool:
        """
        returns `True` if mail was sent, `False` otherwise.
        :param email_to:
        :param subject:
        :param body:
        :return:
        """
        return self.Email()\
            .set_settings(self.settings)\
            .set_body(body)\
            .set_subject(subject)\
            .set_email_to(email_to)\
            .send()

    def send_mail(self, email_to: str, subject: str, body: str) -> bool:
        """
        returns `True` if mail was sent, `False` otherwise.
        :param email_to:
        :param subject:
        :param body:
        :return:
        """
        return self._send_mail(email_to, subject, body)

    def send_mail_to_self(self, subject: str, body: str) -> bool:
        """
        returns `True` if mail was sent, `False` otherwise.
        :param subject:
        :param body:
        :return:
        """
        email_to = self.email_user
        return self.send_mail(email_to, subject, body)

    @staticmethod
    def create_email_secret(email: str):
        """Создает из адреса почты секрет (для базы данных)."""
        return md5(f'{str(uuid.uuid4())}{email}'.encode()).hexdigest()

    async def create_password_refresh(self, secret: str, email: str) -> EmailPasswordRefreshServiceModel:
        """
        Create EmailPasswordRefresh in db.
        :raise EmailPasswordRefreshAlreadyExistsException:
        :param secret:
        :param email:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            email_password_refresh = EmailPasswordRefresh(secret=secret, email=email)
            try:
                session.add(email_password_refresh)
                await session.commit()
                await session.refresh(email_password_refresh)
            except IntegrityError:
                raise EmailPasswordRefreshAlreadyExistsException
        return EmailPasswordRefreshServiceModel.model_validate(email_password_refresh)

    async def delete_by_email_email_password_refresh(self, email: str):
        """
        Delete EmailPasswordRefresh objects with emails == `email`. If there are no EmailPasswordRefresh,
        do nothing.
        :param email:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            prs = (await session.execute(
                sa.select(EmailPasswordRefresh).where(EmailPasswordRefresh.email == email)
            )).scalars().all()
            for pr in prs:
                await session.delete(pr)
            await session.commit()

    async def get_by_secret_email_password_refresh(self, secret: str) -> EmailPasswordRefreshServiceModel:
        """
        :raise EmailPasswordRefreshNotFoundException:
        :param secret:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            pr = (await session.execute(
                sa.select(EmailPasswordRefresh)
                .where(EmailPasswordRefresh.secret == secret)
            )).scalar()
            if pr is None:
                raise EmailPasswordRefreshNotFoundException
        return EmailPasswordRefreshServiceModel.model_validate(pr)

    async def create_email_subscriber(self, secret: str, email: str) -> EmailSubscriberRefreshServiceModel:
        """
        Create EmailPasswordRefresh in db.
        :raise EmailSubscriberAlreadyExistsException:
        :param secret:
        :param email:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            email_subscriber = EmailSubscriber(secret=secret, email=email)
            try:
                session.add(email_subscriber)
                await session.commit()
                await session.refresh(email_subscriber)
            except IntegrityError:
                raise EmailSubscriberAlreadyExistsException
        return EmailSubscriberRefreshServiceModel.model_validate(email_subscriber)

    async def delete_by_secret_email_subscriber(self, secret: str):
        """
        :raise EmailSubscriberNotFoundException:
        :param secret:
        :return:
        """
        async with self.async_session() as session:
            session: AsyncSession
            subscriber = (await session.execute(
                sa.select(EmailSubscriber).where(EmailSubscriber.secret == secret)
            )).scalars().first()
            if subscriber is None:
                raise EmailSubscriberNotFoundException
            await session.delete(subscriber)
            await session.commit()
