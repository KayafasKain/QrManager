# QrManager
## Модели
### Нюнас связанный с типами кодов
Вся информация о qr коде, за исключением статистических данных, хранится в одном отношении **QrCode**. Я решил пойти на денормализацию, ради производительности, на пример, можно было бы вынести в отдельную таблицу информацию о типе кода, однако при выполнении любых операций нам пришлось бы делать дополнительный запрос в базу даных, более того сама предметная область не предпологает болтшого количества типов qr кодов. Таким образом логика контроля типов (валидация соответствия содержимого кода его типу) была реализована в коде, с помощью словаря и регулярных выражений.
### Статистика
Статистические даные хранятся в отдельной таблице **QrStats** и представляет собой журнал посещений эндпоинта **codes/scan**. Когда нужно получить статистику сканирований кода, производится выборка и подсчет релевантных записей.

