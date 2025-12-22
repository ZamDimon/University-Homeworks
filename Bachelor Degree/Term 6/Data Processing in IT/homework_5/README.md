# :spiral_notepad: Завдання

1. Запустити IDE
2. У новому документі `aboutme.html` оформити інформацію наступним чином:
    - Прізвище, ім'я
    - факультет група
    - Про себе
    - Знання IT технологій (мови, баз даних комп'ютерні програми)
    - Захоплення
    - Фон
3. Для роботи з зображенням знайдіть на диску потрібну Вам картинку і
скопіюйте її в свою папку. Для своєї сторінки встановити фон. Додайте своє
фото.
4. Розділ «Про себе» повинен бути написаний 12 шрифтом, колір встановити
на свій розсуд, шрифт - напівжирний курсив.
5. Назву факультету і групи оформити її у вигляді рядка, що біжить.
6. Знання IT технологій позначити цифрами (нумерованим списком), вони
повинні бути написані 10 розміром шрифту, колір вибрати на свій розсуд.
7. Хобі оформити у вигляді ненумерованого списку, 10 розміром шрифту, колір
вибрати на свій розсуд.
8. Пiд прізвищем та ім'ям провести лінію червоного кольору, ширина якої
дорівнює 5, на всю сторінку.
9. Внизу сторінки провести лінію такої ж товщини, під якою написати справа
адресу своєї електронної пошти.

## :white_check_mark: Відповідь

Всі завдання виконаємо одразу. Для цього відкриємо Visual Studio Code та створимо новий файл `aboutme.html`. Введемо наступний код:

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
                font-size: 12pt;
                font-weight: 600;
                font-style: italic;
            }
            .name {
                color: lightgray;
                font-weight: bold;
                font-size: 20pt;
                font-family: 'Arial Black';
            }
            ol, li {
                color: lightgray;
                font-size: 10pt;
            }
            .email {
                text-align: right;
                font-size: 14pt;
            }
        </style>
        <title>Прикладна математика</title>
    </head>
    <!-- Head declaration and such above -->
    <body>
        <h2 class="name">Dmytro Zakharov</h2>
        <hr size="5" align="left" color="red">
        <marquee class="name" direction="right" bgcolor="gray">Applied Mathematics, Group 3-1</marquee>
        <p><strong>About me:</strong> Student majoring in Applied Mathematics and R&D Engineer at Distributed Lab. Passionate about Cryptography, Deep Learning, and Mathematics.</p>
        <p><strong>Programming languages:</strong> 
            <ol>
                <li>Rust</li>
                <li>Golang</li>
                <li>Python</li>
                <li>C++</li>
                <li>Javascript</li>
                <li>C#</li>
                <li>Java</li>
            </ol>
        <p><strong>Additional tools and frameworks:</strong>
            <ol>
                <li>Wolfram Mathematica</li>
                <li>LaTeX</li>
                <li>Sagemath</li>
                <li>Tensorflow</li>
                <li>Keras</li>
            </ol>
        <p><strong>Hobbys:</strong> 
            <ul>
                <li>Applied Cryptography</li>
                <li>Machine Learning</li>
                <li>Elliptic Curve Optimizations</li>
                <li>Computer Vision</li>
                <li>Biometric systems</li>
            </ul>
        <hr size="5" align="left" color="red">
        <p class="email"><strong>Email:</strong> zamdmytro@gmail.com</p>
    </body>
</html>
```

Коментарі по кожному з питань:

1. IDE я при цьому запустив :)
2. Всю інформацію наведену вказано.
3. Єдине, свою фотографію я не завантажував, бо соромно :(
4. Наведений стиль вказаний у пункті `p {...}` в `<style>`.
5. Назва факультету та групи вказана у вигляді рядка, що біжить за допомогою тегу `<marquee>`.
6. Знання IT технологій вказані у вигляді нумерованого списку за допомогою тегу `<ol>`. Розмір шрифта також вказаний у пункті `ol, li {...}` в `<style>`.
7. Хобі вказані у вигляді ненумерованого списку за допомогою тегу `<ul>`. Розмір шрифта також вказаний у пункті `ol, li {...}` в `<style>`.
8. Лінія під прізвищем та ім'ям вказана червоного кольору, шириною 5 пікселів за допомогою тегу `<hr>`.
9. Лінія внизу сторінки вказана червоного кольору, шириною 5 пікселів за допомогою тегу `<hr>`. Адреса електронної пошти вказана справа від лінії, вирівняна по правому краю та написана шрифтом 14 пунктів: стиль вказаний у класі `.email`.
