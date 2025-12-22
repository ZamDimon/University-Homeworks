# :spiral_notepad: Завдання

1. Запустити IDE і відкрити документ index.html.
2. Змінити документ так, щоб напис «Харківський національний університет»
був заголовком першого рівня і був вирівняний по центру,
3. Додати назву факультету та спеціальності - заголовком другого та
третього рівня, також вирівняти по центру.
4. Додати в документ параграф: Прiзвище, Iм'я, по батьковi
5. Додати в документ два параграфи про себе
6. Перший параграф вирівняти по правому краю та встановити для слова
розмір 5
7. Для третього параграфа: розмір 4
8. Для свого прізвища, імен, по батькові встановити шрифт Arial Black.
9. Підкреслити якусь стрiчку в текстi
10. Великим шрифтом виділити факультет, курсивом - спеціальність.
11. Подивитися на зміни за допомогою браузера або Live Server.

## :white_check_mark: Відповідь

1. Відкриваємо Visual Studio Code.
2. З минулого завдання ми вже зробили його заголовком першого рівня, тому залишилось лише відцентрувати. Для цього додамо тег `<center>`:

    ```html
    ...
    <body>
        <center><h1>V.N. Karazin Kharkiv National University</h1></center>
    </body>
    ```

3. Додамо дві додаткові назви і поставимо їх під тег `<center>`:

    ```html
    <!-- Head declaration and such above -->
    <body>
        <center>
            <h1>V.N. Karazin Kharkiv National University</h1>
            <h2>School of Mathematics and Informatics</h2>
            <h3>Applied Mathematics Department</h3>
        </center>
    </body>
    ```

4-5. Як і просили, додаємо параграфи з ім'ям, виділеним жирним за допомогою тегу `<strong>`, а також два параграфи про себе:

```html
    <!-- Head declaration and such above -->
    <body>
        <center>
            <h1>V.N. Karazin Kharkiv National University</h1>
            <h2>School of Mathematics and Informatics</h2>
            <h3>Applied Mathematics Department</h3>
        </center>

        <p><strong>Dmytro Zakharov</strong></p>
        <p>Applied Mathematics student at Karazin National University. 
            Research and Development Engineer at Distributed Lab.</p>
        <p>Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
    </body>
    ```

6. Для першого параграфу вирівняємо його по правому краю та встановимо розмір 5:

    ```html
    <!-- Head declaration and such above -->
    <body>
        <center>
            <h1>V.N. Karazin Kharkiv National University</h1>
            <h2>School of Mathematics and Informatics</h2>
            <h3>Applied Mathematics Department</h3>
        </center>

        <p style="text-align: right; font-size: 5em;"><strong>Dmytro Zakharov</strong></p>
        <p>Applied Mathematics student at Karazin National University. 
            Research and Development Engineer at Distributed Lab.</p>
        <p>Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
    </body>
    ```

7. Для третього параграфу встановимо розмір 4:

    ```html
    <!-- Head declaration and such above -->
    <body>
        <center>
            <h1>V.N. Karazin Kharkiv National University</h1>
            <h2>School of Mathematics and Informatics</h2>
            <h3>Applied Mathematics Department</h3>
        </center>

        <p style="text-align: right; font-size: 5em;"><strong>Dmytro Zakharov</strong></p>
        <p>Applied Mathematics student at Karazin National University. 
            Research and Development Engineer at Distributed Lab.</p>
        <p style="font-size: 4em;">Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
    </body>
    ```

8. Для свого прізвища, імен, по батькові встановимо шрифт Arial Black:

    ```html
    <!-- Head declaration and such above -->
    <body>
        <center>
            <h1>V.N. Karazin Kharkiv National University</h1>
            <h2>School of Mathematics and Informatics</h2>
            <h3>Applied Mathematics Department</h3>
        </center>

        <p style="text-align: right; font-size: 5em;"><strong><span style="font-family: 'Arial Black';">Dmytro Zakharov</span></strong></p>
        <p>Applied Mathematics student at Karazin National University. 
            Research and Development Engineer at Distributed Lab.</p>
        <p style="font-size: 4em;">Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
    </body>
    ```

9. Підкреслимо назви університету та компанії Distributed Lab у параграфах за допомогою тегу `<u>`:

    ```html
    <!-- Head declaration and such above -->
    <body>
        <center>
            <h1>V.N. Karazin Kharkiv National University</h1>
            <h2>School of Mathematics and Informatics</h2>
            <h3>Applied Mathematics Department</h3>
        </center>

        <p style="text-align: right; font-size: 5em;"><strong><span style="font-family: 'Arial Black';">Dmytro Zakharov</span></strong></p>
        <p>Applied Mathematics student at <u>Karazin National University</u>. 
            Research and Development Engineer at <u>Distributed Lab</u>.</p>
        <p style="font-size: 4em;">Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
    </body>
    ```

10. Великим шрифтом виділимо факультет, курсивом - спеціальність в параграфі:

    ```html
    <!-- Head declaration and such above -->
    <body>
        <center>
            <h1>V.N. Karazin Kharkiv National University</h1>
            <h2>School of Mathematics and Informatics</h2>
            <h3>Applied Mathematics Department</h3>
        </center>

        <p style="text-align: right; font-size: 5em;"><strong><span style="font-family: 'Arial Black';">Dmytro Zakharov</span></strong></p>
        <p><em>Applied Mathematics</em> student at <u>Karazin National University</u>, <big>School of Mathematics and Informatics</big>. Research and Development Engineer at <u>Distributed Lab</u>.</p>
        <p style="font-size: 4em;">Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
    </body>
    ```
11. Зберігли зміни та перевірили їх за допомогою Live Server. Ітоговий код:

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
                h1, h2, h3, p {
                    color: rgb(245, 245, 245);
                }
            </style>
            <title>Прикладна математика</title>
        </head>
        <!-- Head declaration and such above -->
        <body>
            <center>
                <h1>V.N. Karazin Kharkiv National University</h1>
                <h2>School of Mathematics and Informatics</h2>
                <h3>Applied Mathematics Department</h3>
            </center>

            <p style="text-align: right; font-size: 5em;"><strong><span style="font-family: 'Arial Black';">Dmytro Zakharov</span></strong></p>
            <p><em>Applied Mathematics</em> student at <u>Karazin National University</u>, <big>School of Mathematics and Informatics</big>. Research and Development Engineer at <u>Distributed Lab</u>.</p>
            <p style="font-size: 4em;">Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
        </body>
    </html>
    ```
