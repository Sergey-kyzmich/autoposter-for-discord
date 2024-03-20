# Autoposter for discord by Kyzmich on python
Автопостер выполнен в виде **discord бота**. Взаимодействие происходит через личные сообщения с ботом.

## Как запустить?
1) Для запуска требуется получить токен бота на [портале discord](https://discord.com/developers/)
2) Затем бота требуется добавить на ваш сервер discord.
3) Записать токен бота в файле auto_poster_bot.py в 97 строке
```
config = {
    'token': ''
    'prefix': '/',
}
```
4) Ключи активации подписки лежат в файлах token_07_day.txt, token_30_day.txt, token_99_day.txt

## команды бота
1) /menu - основное меню бота
2) /help - меню с перечнем команд
3) /instruction - Инструкция по использованию
4) /buy - команда для активации подписки

## Используемые библиотеки
1) discord
2) py-cord(v2.4.1)
3) requests
4) sys
5) os
6) datetime
7) time
8) subprocess
9) json
10) websocket
