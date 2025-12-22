# :spiral_notepad: Завдання

1. У файл `index.html` додати абзац «Iнформацію про мене, мої знання і
захоплення можна подивитися тут».
2. На початку файлу `about_me.html` фразу «Про себе» укласти в теги `<a name="info">`
і `</a>`.
3. У документі `main.html` слово «тут» оформити гіперпосиланням на документ
`about_me.html` на якір «info»
4. Змінити колір невідвіданих гіперпосилань на синій, а відвіданих на сірий.
5. Випробувати дію гіперпосилання.
6. Оформити електронну пошту у вигляді посилання для відправки писати.
7. У файл `about_me.html` внизу сторінки помістити абзац, що складається з одного слова «Назад», вирівняного по центру.
8. Організувати зворотний перехід.
9. Завдання: в документ `main.html` додати абзаци
    - «Тут ви можете подивитися сайт ХНУ».
    - «Тут ви можете подивитися сайт інтернет-магазину Rozetka».
10. Оформити кольорово абзаци на свій розсуд.
11. Оформити абзаци як гіперпосилання на сайти ХНУ і Rozetka.

## :white_check_mark: Відповідь

1. Додаємо наступний параграф:

    ```html
    <!-- Some code above --->
    <p>
        Information about me, my skills, and my hobbys can be found here.
    </p>
    <!-- Some code below --->
    ```

2. Тепер строчка з "About me" виглядає наступним чином:

    ```html
    <!-- Some code above --->
    <p><strong><a name="info">About me:</a></strong> Student majoring in Applied Mathematics and R&D Engineer at Distributed Lab. Passionate about Cryptography, Deep Learning, and Mathematics.</p>
    <!-- Some code below --->
    ```

3. Робимо гіперпосилання:

    ```html
    <!-- Some code above --->
    <p>
        Information about me, my skills, and my hobbys can be found <a href="about_me.html#info">here</a>.
    </p>
    <!-- Some code below --->
    ```

4. Зробимо це за допомогою стилю:

    ```css
    a:link {
        color: blue;
    }
    a:visited {
        color: gray;
    }
    ```

5. Працює, перевірено.
6. Замінимо строчку з e-mail на наступну (тепер по пошті можна натиснути):

    ```html
    <p class="email"><strong>Email:</strong> <a href="mailto:zamdmytro@gmail.com">zamdmytro@gmail.com</a></p>
    ```

7. Додамо клас `back`, в якому стиль задамо достатньо просто:

    ```css
    .back {
        text-align: center;
        font-size: 14pt;
        font-weight: bold;
    }
    ```

    Саму кнопку оформимо, як і сказано, в абзаці:

    ```html
    <p class="back"><a href="index.html">Return to the main page</a></p>
    ```

8. Зворотний перехід реалізований за допомогою атрибуту `href="index.html"` у тегу `<a>`.
9-11. Додамо абзаци наступним чином:

    ```html
        <p>
            <a href="https://karazin.ua/">Here</a> you can navigate to the V.N. Karazin Kharkiv National University website.
        </p>
        <p>
            <a href="https://rozetka.com.ua/ua/">Here</a> you can navigate to Rozetka store.
        </p>
    ```
