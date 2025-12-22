# :spiral_notepad: Завдання

1. На жорсткому диску створити папку з ім'ям HTML.
2. Відкрити IDE або текстовий редактор "Блокнот".
3. У вікні блокнота створити документ, що друкує в якості заголовка документа
назву Вашої спеціальності.
4. Зберегти документ під ім'ям index.html, обов'язково з розширенням html в папці
HTML.
5. Запустити Live Server або відкрити документ, використовуючи будь-який з
браузерів, встановлений в системі, наприклад,Chrome.
6. Використовуючи меню Файл - Відкрити, відкрити у вікні браузера свій файл і
переконатися, що в рядку заголовка надруковано назву Вашої спеціальності.
7. Перейти в вікно редактора Блокнот і додати у вікні браузера напис
«Харківський національний університет».
8. Збережіть зміни.
9. Перейти в вікно браузера, щоб переглянути внесені зміни, необхідно натиснути
кнопку "Оновити".
10. Використовуючи метадані, визначити автора документа і ключові слова: назва
Вашої спеціальності і назву вашого факультету.
11. Установити бiлий колір фону документа на свій смак.
12. Встановити фонову картинку, для цього:
    - на жорсткому диску знайти файл з розширенням jpg. png або gif;
    - скопіювати знайдений файл в свою папку;
    - встановити фонову картинку;
13.Зберегти результати, так як такі завдання спираються на результати
попередніх.

## :white_check_mark: Відповідь

1. Створюємо папку на жорсткому диску. Проте, я його поклав з назвою `homework_2`, оскільки так зручніше для сортування завдань.
2. Відкриваємо Visual Studio Code.
3. Введемо наступний код:

    ```html
    <!DOCTYPE html>

    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Прикладна математика</title>
        </head>
        <body>
            
        </body>
    </html>
    ```

4. Зберегли.
5. Запустили Live Server.
6. Переконалися, що в рядку заголовка надруковано назва "Прикладна математика".
7. Додамо опис у вигляді заголовку `<h1>`. Також додамо метадані з автором та ключовими словами:

    ```html
    <!DOCTYPE html>

    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="Dmytro Zakharov">
            <meta name="keywords" content="applied mathematics, khnu">
            <title>Applied Mathematics</title>
        </head>
        <body>
            <h1>V.N. Karazin Kharkiv National University</h1>
        </body>
    </html>
    ```

8. Зберегли зміни.
9. Натиснули кнопку "Оновити".
10. Додали у пункті 8.
11. Встановимо білий колір фону документа: додаємо стиль `style="background-color:white;"` до тегу `<body>`.

    ```html
    <!DOCTYPE html>

    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="Dmytro Zakharov">
            <meta name="keywords" content="applied mathematics, khnu">
            <title>Applied Mathematics</title>
        </head>
        <body style="background-color:white;">
            <h1>V.N. Karazin Kharkiv National University</h1>
        </body>
    </html>
    ```

12-13. Додаємо картинку на фон. Також, ми одразу під тегом `<style>` задаємо стилі для елементів: оскільки фон темний, то текст ми зробимо білим.

```html
    <!DOCTYPE html>

    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="Dmytro Zakharov">
            <meta name="keywords" content="applied mathematics, khnu">
            <style>
                /* Background image taken from https://github.com/brave/brave-browser/issues/8061 */
                body {
                    background-image: url('background.png');
                    background-repeat: no-repeat;
                    background-size: cover;
                }
                h1 {
                    color: rgb(245, 245, 245);
                    font-size: 3em;
                }
            </style>
            <title>Applied Mathematics</title>
        </head>
        <body>
            <h1>V.N. Karazin Kharkiv National University</h1>
        </body>
    </html>
    ```
