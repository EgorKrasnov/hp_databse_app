Для запуска Dev выполните
docker-compose -f docker-compose.dev.yml up -d
docker exec -it working_with_DB_dev python /usr/src/app/main.py

Перед запуском Prod версии необходимо убедиться в том, что прошлый контейнер был остановлен и удален.
Иначе Prod подгрузит базу данных из Dev контейнера!
Выпоните команды
docker kill working_with_DB_dev postgres
docker rm working_with_DB_dev postgres

Для запуска Prod версии выполните
docker-compose -f docker-compose.prod.yml up -d
docker exec -it working_with_DB_prod python /usr/src/app/main.py

При первом старте Prod версии на вашем компьютере необходимо наполнить базу данных.
Вы можете сделать это вручную или выполнив команду python скрипта "fill"

Чтобы закрыть и удалить контейнеры выполните
docker kill working_with_DB_prod postgres
docker rm working_with_DB_prod postgres

