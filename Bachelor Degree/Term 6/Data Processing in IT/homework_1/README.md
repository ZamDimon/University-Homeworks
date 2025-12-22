# :spiral_notepad: Завдання

1. Ознайомитися з базовою інформацією про мову
2. Ознайомитися з основними тегами мови
3. Скласти таблицю основних тегів і їх призначень
4. Відкрити у вікні браузера сторінку улюбленого сайту в моді розробника і
подивитися на структуру реального документа спробувати зрозуміти, що що i як буде
відображено, вивчити структуру документа.
5. Порівняти будь-які два сайти в моді розробника та спробувати знайти спільні та
обов`язкові елементи документів HTML-сторінок
6. Подивитись, яку інформацію місить секція head документу та як вона використана.
7. Встановити обладнання для виконання наступних лабораторних:
    - Visual Studio Code
    - Live Server Extension

## :white_check_mark: Відповідь

### Питання 3

У найновішій версії HTML (5.2) формально нараховується 142 теги. Тому, ми не будемо переховувати усі можливі теги і зосередимось на тих, які використовуються найчастіше.

Отже, знизу ми наводимо самі теги, деякі їх атрибути та призначення:

| Тег | Приклад | Призначення |
| --- | --- | --- |
| `<!DOCTYPE html>` | `<!DOCTYPE html>` | Визначає тип документа |
| `<html>` | `<html lang="en">` | Визначає початок HTML документа |
| `<head>` | `<head>` | Визначає інформацію про документ |
| `<title>` | `<title>Document</title>` | Визначає заголовок документа |
| `<body>` | `<body>` | Визначає тіло документа |
| `<h1> - <h6>` | `<h1>Header</h1>` | Визначає заголовок |
| `<p>` | `<p>Paragraph</p>` | Визначає абзац |
| `<br>` | `<br>` | Визначає перенесення рядка |
| `<hr>` | `<hr>` | Визначає горизонтальну лінію |
| `<a>` | `<a href="https://www.google.com">Google</a>` | Визначає посилання |
| `<img>` | `<img src="image.jpg" alt="Image">` | Визначає зображення |
| `<ul>` | `<ul><li>Item</li></ul>` | Визначає ненумерований список |
| `<ol>` | `<ol><li>Item</li></ol>` | Визначає нумерований список |
| `<li>` | `<li>Item</li>` | Визначає елемент списку |
| `<table>` | `<table><tr><td>Row</td></tr></table>` | Визначає таблицю |
| `<tr>` | `<tr><td>Row</td></tr>` | Визначає рядок таблиці |
| `<td>` | `<td>Row</td>` | Визначає комірку таблиці |
| `<th>` | `<th>Header</th>` | Визначає заголовок таблиці |
| `<form>` | `<form action="/submit" method="post">Form</form>` | Визначає форму |
| `<input>` | `<input type="text">` | Визначає поле вводу |
| `<button>` | `<button>Button</button>` | Визначає кнопку |
| `<label>` | `<label for="input">Label</label>` | Визначає підпис |
| `<select>` | `<select><option>Option</option></select>` | Визначає список |
| `<option>` | `<option>Option</option>` | Визначає елемент списку |
| `<textarea>` | `<textarea>Text</textarea>` | Визначає текстове поле |
| `<div>` | `<div>Division</div>` | Визначає розділ |
| `<span>` | `<span>Span</span>` | Визначає рядок |
| `<iframe>` | `<iframe src="https://www.google.com"></iframe>` | Визначає фрейм |
| `<audio>` | `<audio src="audio.mp3"></audio>` | Визначає звук |
| `<video>` | `<video src="video.mp4"></video>` | Визначає відео |
| `<canvas>` | `<canvas></canvas>` | Визначає малюнок |

### Питання 4

Один з моїх улюблених сайтів -- GitHub. Я відкрив його в моді розробника та подивився на структуру документа. Якщо говорити про структуру, то вона виглядає наступним чином:

```html
<!DOCTYPE html>
<html
  lang="en"
  data-color-mode="dark" data-light-theme="light" data-dark-theme="dark_dimmed"
  data-a11y-animated-images="system" data-a11y-link-underlines="true">

<head>
    <meta charset="utf-8">
    <link rel="dns-prefetch" href="https://github.githubassets.com">
    <link rel="dns-prefetch" href="https://avatars.githubusercontent.com">
    <link rel="dns-prefetch" href="https://github-cloud.s3.amazonaws.com">
    <link rel="dns-prefetch" href="https://user-images.githubusercontent.com/">
    <link rel="preconnect" href="https://github.githubassets.com" crossorigin>
    <link rel="preconnect" href="https://avatars.githubusercontent.com">

  ... (a lot of links)

    <script type="application/json" id="client-env">{"locale":"en","featureFlags":["code_vulnerability_scanning","copilot_chat_static_thread_suggestions","copilot_chat_in_mobile_ga","copilot_conversational_ux_history_refs","copilot_followup_to_agent","copilot_smell_icebreaker_ux","copilot_implicit_context","copilot_stop_response","copilot_updated_function_buttons","failbot_handle_non_errors","geojson_azure_maps","image_metric_tracking","marketing_forms_api_integration_contact_request","marketing_pages_search_explore_provider","repository_suggester_elastic_search","turbo_experiment_risky","sample_network_conn_type","no_character_key_shortcuts_in_inputs","react_start_transition_for_navigations","custom_inp","remove_child_patch","kb_source_repos"]}</script>
    <script crossorigin="anonymous" defer="defer" type="application/javascript" src="https://github.githubassets.com/assets/wp-runtime-8e2c3fd7c7ca.js"></script>
    <script crossorigin="anonymous" defer="defer" type="application/javascript" src="https://github.githubassets.com/assets/vendors-node_modules_dompurify_dist_purify_js-810e4b1b9abd.js"></script>
    <script crossorigin="anonymous" defer="defer" type="application/javascript" src="https://github.githubassets.com/assets/vendors-node_modules_stacktrace-parser_dist_stack-trace-parser_esm_js-node_modules_github_bro-6663c5-f997ed3e81d6.js"></script>

    ... (a lot of scripts)

    <script crossorigin="anonymous" defer="defer" type="application/javascript" src="https://github.githubassets.com/assets/dashboard-e10185c9be10.js"></script>

    <title>GitHub</title>

    <meta name="route-pattern" content="/" data-turbo-transient>
    <meta name="route-controller" content="dashboard" data-turbo-transient>
    <meta name="route-action" content="index" data-turbo-transient>
    <meta name="current-catalog-service-hash" content="40dc28bd654b20f337468a532ff456ed5863889cfbb4e982b793597321d48d3f">

    ... (a lot of meta)
    
<body class="logged-in env-production page-responsive full-width" style="word-wrap: break-word;">
    <div data-turbo-body class="logged-in env-production page-responsive full-width" style="word-wrap: break-word;">
      
    <div class="position-relative js-header-wrapper ">
        <a href="#start-of-content" data-skip-target-assigned="false" class="p-3 color-bg-accent-emphasis color-fg-on-emphasis show-on-focus js-skip-to-content">Skip to content</a>
      
        <span data-view-component="true" class="progress-pjax-loader Progress position-fixed width-full">
    <span style="width: 0%;" data-view-component="true" class="Progress-item progress-pjax-loader-bar left-0 top-0 color-bg-accent-emphasis"></span>
</span>      
      
<script crossorigin="anonymous" defer="defer" type="application/javascript" src="https://github.githubassets.com/assets/react-lib-dc88c1a68b28.js"></script>
... (a lot of scripts)
<script crossorigin="anonymous" defer="defer" type="application/javascript" src="https://github.githubassets.com/assets/keyboard-shortcuts-dialog-52a107eb77ae.js"></script>

<react-partial
  partial-name="keyboard-shortcuts-dialog"
  data-ssr="false"
>
  
<script type="application/json" data-target="react-partial.embeddedData">{"props":{"docsUrl":"https://docs.github.com/get-started/accessibility/keyboard-shortcuts"}}</script>
  <div data-target="react-partial.reactRoot"></div>
</react-partial>
<script crossorigin="anonymous" defer="defer" type="application/javascript" src="https://github.githubassets.com/assets/vendors-node_modules_allex_crc32_lib_crc32_esm_js-node_modules_github_mini-throttle_dist_deco-a9eeba-34e4d091ae23.js"></script>
... (a lot of scripts)
<script crossorigin="anonymous" defer="defer" type="application/javascript" src="https://github.githubassets.com/assets/command-palette-a99cf9e9f4ca.js"></script>

    <header class="AppHeader" role="banner">
    <h2 class="sr-only">Navigation Menu</h2>

    <div class="AppHeader-globalBar  js-global-bar">
    <div class="AppHeader-globalBar-start">
    <deferred-side-panel data-url="/_side-panels/global">
    <include-fragment data-target="deferred-side-panel.fragment">
        <button aria-label="Open global navigation menu" data-action="click:deferred-side-panel#loadPanel click:deferred-side-panel#panelOpened" data-show-dialog-id="dialog-f30f172f-7c9e-437a-865b-d69ab6b0d8eb" id="dialog-show-dialog-f30f172f-7c9e-437a-865b-d69ab6b0d8eb" type="button" data-view-component="true" class="Button Button--iconOnly Button--secondary Button--medium AppHeader-button color-bg-transparent p-0 color-fg-muted">  <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-three-bars Button-visual">
    <path d="M1 2.75A.75.75 0 0 1 1.75 2h12.5a.75.75 0 0 1 0 1.5H1.75A.75.75 0 0 1 1 2.75Zm0 5A.75.75 0 0 1 1.75 7h12.5a.75.75 0 0 1 0 1.5H1.75A.75.75 0 0 1 1 7.75ZM1.75 12h12.5a.75.75 0 0 1 0 1.5H1.75a.75.75 0 0 1 0-1.5Z"></path>
    </svg>
        </button>
```

### Питання 5

Отже бачимо, шо структура приблизно наступна:

- `<!DOCTYPE html>` - визначає тип документа
- `<html>` - визначає початок HTML документа
- `<head>` - визначає інформацію про документ
- `<title>` - визначає заголовок документа
- `<body>` - визначає тіло документа

## Питання 6

Секція `head` документу містить інформацію про документ, яка не відображається на сторінці. Вона містить метатеги, які визначають заголовок документа, зовнішні стилі, скрипти, метатеги для пошукових систем, автора, ключові слова та іншу інформацію.

## Питання 7

Зроблено
