Описание проекта Новостной портал

Проект в котором собраны новости с разным сайтов


1. На главной странице показаны последние 10 новостей
2. Есть возможность добавления комментариев
3. Добавлять, редактировать и удалять новости могут только авторы
4. Есть поиск по новостям
5. Есть возможность выбирать новости по категориям
6. Реализована возможность авторизации через Google-аккаунт
7. Реализована возможность подписаться/отписаться от новостей
8. Если пользователь подписан на какую-либо категорию, то, как только в неё добавляется новая статья, её краткое содержание приходит пользователю на электронную почту, которую он указал при регистрации.
9. Подтверждение регистрации по email
10. Установлено ограничение на 3 новости в сутки
11. Если пользователь подписан на какую-либо категорию, то каждую неделю ему приходит на почту список новых статей, появившихся за неделю
12. Автоматический сбор новостей - каждые 6 часов
13. По понедельникам в 8:00 рассылаются новости за прошедшую неделю
14. Добавлено кэширование главной страницы, страницы с категориями новостей, а также кэширование нвоости до изменения



Можно запустить задачу сбора новостей вручную
запускаем консоли и пишем:
py manage.py shell
from news.tasks import run_news_parser
run_news_parser()


Работа с Celery
В одной консоле запускаем celery -A NewsPaper beat
В другой консоле запускаем celery -A NewsPaper worker --loglevel=INFO --concurrency 1 -P solo