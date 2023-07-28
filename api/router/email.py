from fastapi import APIRouter, HTTPException, Depends, Response
from loguru import logger

from api.context import AppContext
from api.dependencies import get_app_context
from api.schema.email import EmailSuggestionsRequest, EmailOfferObjectRequest, EmailSubscribeRequest, \
    PasswordRefreshRequest

router = APIRouter(
    prefix='/email',
    tags=['Email']
)


@router.post('/suggestions')
async def send_email_suggestions(
    body: EmailSuggestionsRequest,
    app_context: AppContext = Depends(get_app_context),
):
    if body.text is None or body.text == '':
        return
    email_subject = 'Пожелания и замечания'
    email_body = f'Пользователь {body.first_name} {body.last_name} <{body.email}> отправил пожелание:\n\n' \
                 f'{body.text if body.text is not None else ""}'
    app_context.email_service.send_mail_to_self(email_subject, email_body)


@router.post('/offer-object')
async def offer_object_with_email(
    body: EmailOfferObjectRequest,
    app_context: AppContext = Depends(get_app_context),
):
    if body.note is None:
        body.note = ''
    email_subject = 'Предложение нового объекта'
    email_body = f'Поступило предложение нового объекта:\n\n' \
                 f'Адрес - {body.address}\nВладелец - {body.owner}\nПримечание - {body.note}'
    app_context.email_service.send_mail_to_self(email_subject, email_body)


@router.post('/subscribe')
async def email_subscribe(
    body: EmailSubscribeRequest,
    app_context: AppContext = Depends(get_app_context),
):
    secret = app_context.email_service.create_email_secret(body.email)
    subscribe = await app_context.email_service.create_email_subscriber(secret, body.email)

    logger.debug(f'SUBSCRIBE {body.email} {secret}')

    # TODO: переместить в settings
    unsubscribe_link = f'https://sportsmap.spb.ru/new-api/v1/email/unsubscribe/{secret}'

    email_subject = 'Подписка на новости SportsMap'
    email_body = \
        f'Здравствуйте. Вы подписались на новости SportsMap. ' \
        f'Теперь при добавлении новых спортивных объектов мы вас проинформируем.\n' \
        f'Чтобы отписаться, пройдите по ссылке: {unsubscribe_link}'

    app_context.email_service.send_mail(body.email, email_subject, email_body)


@router.get('/unsubscribe/{secret}')
async def email_unsubscribe(
    secret: str,
    app_context: AppContext = Depends(get_app_context),
):
    try:
        deleted = await app_context.email_service.delete_by_secret_email_subscriber(secret)
    except Exception as e:
        logger.warning(e)
        return Response("Вы не подписаны на наши обновления".encode('utf-8'), status_code=400, media_type='text/plain')
    if not deleted:
        return Response("Вы не подписаны на наши обновления".encode('utf-8'), status_code=400, media_type='text/plain')
    return Response("Вы отписались от наших обновлений".encode('utf-8'), media_type='text/plain')


@router.post('/new-password')
async def refresh_user_password(
    body: PasswordRefreshRequest,
    app_context: AppContext = Depends(get_app_context),
):
    await app_context.user_service.check_exists_by_email(body.email)
    secret = app_context.email_service.create_email_secret(body.email)

    await app_context.email_service.create_password_refresh(secret, body.email)

    # TODO: переместить в settings
    password_link = f'https://sportsmap.spb.ru/new-password?secret={secret}'

    email_subject = 'Изменение пароля SportsMap'
    email_body = \
        f'Здравствуйте. Вы послали запрос на изменение пароля.\n' \
        f'Чтобы изменить пароль, перейдите по ссылке: {password_link}'

    app_context.email_service.send_mail(body.email, email_subject, email_body)
