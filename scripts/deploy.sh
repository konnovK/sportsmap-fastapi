#!/usr/bin/env sh

echo "${OAUTH}" | docker login --username oauth --password-stdin cr.yandex

docker build --tag=cr.yandex/${REGISTRY_ID}/sportsmap-backend-new:v${VERSION} .

docker push cr.yandex/${REGISTRY_ID}/sportsmap-backend-new:v${VERSION}
