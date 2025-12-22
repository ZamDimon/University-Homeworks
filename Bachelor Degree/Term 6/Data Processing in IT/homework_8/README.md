# :spiral_notepad: Завдання

В інтернеті знайти невеличкі файли mp4, і скопіювати один з них в свою папку.
Помістити на сторінку обране відео.

## :white_check_mark: Відповідь

Додамо папку `videos` і додамо туди файл `numbers.mp4`, котрий ми вбудуємо у сайт.

Створюємо окрему сторінку `video.html` з наступним HTML кодом:

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
                background-image: url('images/background.png');
                background-repeat: no-repeat;
                background-size: cover;
            }
            .video {
                display: block;
                margin-left: auto;
                margin-right: auto;
            }
            .back {
                text-align: center;
                font-size: 14pt;
                font-weight: bold;
            }
            .back-img {
                width: 20px;
                height: 20px;
            }
        </style>
        <title>Video</title>
    </head>
    
    <body>
        <embed src="videos/numbers.mp4" class="video"> </embed>

        <p class="back"><a href="index.html"><img src="images/back_icon.png" class="back-img"> Return to the main page</a></p>
    </body>
</html>
```

Маємо звичайну сторінку з вбудованим відео та посиланням на головну сторінку.

На головній сторінці додамо наступну строчку, щоб це відео можна було подивитись:

```html
<p>
    <a href="video.html">Here</a> is an embedded mp4 video.
</p>
```
