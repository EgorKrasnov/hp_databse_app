База данных содержит следующие таблицы: колонки
Герои(Heroes): id, side (сторона, принадлежность), name, birthday
Слоганы героев(Motos): id, hero_id, moto_id (нумерация у каждого героя с 1), moto (текст слогана).
    У каждого героя может быть от 1-го до нескольких слоганов.
Столкновения героев(Fights): id, hero_1_id, hero_1_moto_id (= id таблицы слоганов), hero_2_id, hero_2_moto_id,
    winner (0 для ничьей, 1 для героя 1, 2 для героя 2).
Краткая предыстория героя (Stories): id, hero_id, story.

Перед выполнением docker-compose команд необходимо запустить Docker Desktop

$ Для запуска Dev версии (если есть база, то она удаляется и создаётся/наполняется с нуля) выполните
docker-compose -f docker-compose.dev.yml up -d
docker exec -it working_with_DB_dev python /usr/src/app/main.py

? При возникновении ошибок - убедиться в том, что оба контейнера запущены и работают.
Если это не так, повторить команду docker-compose -f docker-compose.dev.yml up -d

!!! Перед запуском Prod версии необходимо убедиться в том, что прошлый контейнер был остановлен и удален.
Иначе Prod подгрузит базу данных из Dev контейнера!
Выпоните команды
docker kill working_with_DB_dev postgres
docker rm working_with_DB_dev postgres

$ Для запуска Prod версии (база по умолчанию пытается подхватиться существующая) выполните
docker-compose -f docker-compose.prod.yml up -d
docker exec -it working_with_DB_prod python /usr/src/app/main.py

!!! При первом старте Prod версии на вашем компьютере скорость исполнения первой команды меньше, чем Dev версии.
Это займет некоторое время. Если вторая команда не сработала, убедитесь, что оба контейнера работают и повторите запрос.
Также после первого старта необходимо наполнить базу данных. Вы можете сделать это вручную или выполнив команду python скрипта "fill"

По окончанию работы, чтобы закрыть и удалить контейнеры выполните
docker kill working_with_DB_prod postgres
docker rm working_with_DB_prod postgres

Если команда docker exec -it working_with_DB_dev python /usr/src/app/main.py
отработала корректно, то вы увидите интерфейс взаимодействия с БД:

You are welcome in HP database. Please select mode:
1 - add Hero
2 - add Moto
3 - add random Fight!
4 - add Story
5 - delete Hero
6 or q - save & exit
help - for repeat info
heroes - to get id's
fights - to get all fights
motos - to get all motos

Например
После введения  "1" вы увидите "Enter the hero's name"
Необходимо ввести строку, состояющую из имени добавляемого героя. Например "Albus Dumbledore"
Далее вы увидите "Enter the hero's side"
Необходимо ввести строку, состояющую из стороны добавляемого героя. Например "Order of the Phoenix"
Далее вы увидите "Enter the hero's date of birth (YYYY.MM.DD)"
Необходимо ввести строку, состояющую из даты рождения добавляемого героя. Например "1881.8.25"
Далее вы увидите "Hero added!"

Вывести список героев можно выполнив команду "heroes"

