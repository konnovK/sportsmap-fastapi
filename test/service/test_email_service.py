async def test_create_password_refresh(email_service):
    email = "user@example.com"
    secret = email_service.create_email_secret(email)

    print(await email_service.create_password_refresh(secret, email))


async def test_create_subscriber(email_service):
    email = "user@example.com"
    secret = email_service.create_email_secret(email)

    print(await email_service.create_email_subscriber(secret, email))
