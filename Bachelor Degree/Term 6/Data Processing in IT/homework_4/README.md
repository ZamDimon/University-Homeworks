# :spiral_notepad: Завдання

1. Встановити рiзнi кольори для заголовкiв та параграфiв - синій та червоной,
або інші на вибір
2. Використовувати різні способи кодування кольору
3. Намалювати лінію на всю ширину екрану та пофарбувати в зелений колір
4. Зробити рядок Прізвище, ім'я, по батькові, таким, що біжить, встановивши
колір фону gray, напрямок зліва направо.

## :white_check_mark: Відповідь

1. Встановлюємо різні кольори для заголовків та параграфів. Заголовок буде голубого відтінку, а параграф - сірого. Також, частину налаштувань перенесемо у стилі.

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
                h1, h2, h3 {
                    color: rgb(123, 113, 230);
                }
                p {
                    color: lightgray;
                    font-size: 1.5em;
                }
                .name {
                    text-align: right; 
                    font-weight: bold;
                    font-size: 5em;
                    font-family: 'Arial Black';
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

            <p class="name">Dmytro Zakharov</p>
            <p><em>Applied Mathematics</em> student at <u>Karazin National University</u>, <big>School of Mathematics and Informatics</big>. Research and Development Engineer at <u>Distributed Lab</u>.</p>
            <p style="font-size: 4em;">Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
        </body>
    </html>
    ```

2. Голубий відтінок ми задали у RGB форматі, а сірий через вбудований колір (`lightgray`).

3. Намалюємо лінію між заголовками та параграфами і пофарбуємо у зелений колір:

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
                h1, h2, h3 {
                    color: rgb(123, 113, 230);
                }
                p {
                    color: lightgray;
                    font-size: 1.5em;
                }
                .name {
                    text-align: right; 
                    font-weight: bold;
                    font-size: 5em;
                    font-family: 'Arial Black';
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
            
            <hr size="5" width="100" align="left" color="green">
            
            <p class="name">Dmytro Zakharov</p>
            <p><em>Applied Mathematics</em> student at <u>Karazin National University</u>, <big>School of Mathematics and Informatics</big>. Research and Development Engineer at <u>Distributed Lab</u>.</p>
            <p style="font-size: 4em;">Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
        </body>
    </html>
    ```

4. Зробимо рядок прізвище, ім'я, по батькові, таким, що біжить, встановивши
колір фону gray, напрямок зліва направо.

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
                h1, h2, h3 {
                    color: rgb(123, 113, 230);
                }
                p {
                    color: lightgray;
                    font-size: 1.5em;
                }
                .name {
                    color: lightgray;
                    font-weight: bold;
                    font-size: 5em;
                    font-family: 'Arial Black';
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

            <hr size="5" align="left" color="green">
            
            <marquee class="name" direction="right" bgcolor="gray">Dmytro Zakharov</marquee>
            <p><em>Applied Mathematics</em> student at <u>Karazin National University</u>, <big>School of Mathematics and Informatics</big>. Research and Development Engineer at <u>Distributed Lab</u>.</p>
            <p style="font-size: 4em;">Passionate about Cryptography, Deep Learning, Mathematics, and Game Development.</p>
        </body>
    </html>
    ```
