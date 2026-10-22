# Руководство

Это рабочая инструкция. Код, который её исполняет, лежит в `src/mazu_method/`. Если текст и команда расходятся, права команда.

Каждая тема ниже называется так, как её печатает `python3 cli/mazu.py guide ТЕМА`.

## bmad

Ответственность: BMAD lead. Код: `src/mazu_method/bmad.py`.

Делать: держать порядок analysis, planning, solutioning, implementation. Проверять `check phase ИМЯ --outcome "..." --has-boundaries --has-check`.

Не делать: перескакивать в implementation, если нет исхода, границ или способа проверки.

Гейт: команда завершается с кодом 1 и строкой FAIL BMAD-1.

Передача: аналитик даёт исход, автор SDD даёт границы, QA называет проверку.

## sdd

Ответственность: SDD author. Код границ: `src/mazu_method/sdd.py`.

Делать: сначала спецификация из `templates/spec.md`, потом план, потом задачи. Границы писать до кода.

Не делать: расширять историю молча. Не начинать дифф, которого нет в спецификации.

Контроль: `check boundaries ID` и `check guard "действие" --always ... --ask ... --never ...`.

## boundaries

Always проходит. Ask First останавливает процесс, код выхода не ноль, текст начинается с BOUND-2. Never отказывает, текст начинается с BOUND-3. Never сильнее Ask First, Ask First сильнее Always.

Пустые границы — FAIL BOUND-5. Узкий список истории не удаляет Never спецификации: это делает `merge` в коде.

Нельзя считать фразу «сделай как считаешь нужным» снятием гейта.

## bdd

Ответственность: BDD author пишет, QA закрывает. Код: `src/mazu_method/bdd.py`.

Делать: каждый сценарий содержит Given, When и Then. Then называет состояние. Несколько сценариев разделяют `|`.

Не делать: Then из слов «works well», «работает хорошо», «ok», «tbd».

Гейт: `check bdd ID`. До ready нужен хотя бы один сценарий. До done на каждый сценарий нужна улика `evidence ID "текст"`, затем `gate done ID`.

## adr

Ответственность: ADR keeper. Код: `src/mazu_method/adr.py`.

Делать: `add adr "название" --description "факты"`. Файл появляется в `mazu-data/adr/`. В нём четыре части: Status, Context, Decision, Consequences. Пока Decision или Context пустые, `check adr ID` не проходит.

Не делать: удалять старый ADR. Новый файл называет старый id.

## agile

Ответственность: scrum master. Код: `src/mazu_method/agile.py`.

Делать: колонки backlog, ready, in-progress, review, done. В in-progress не больше двух историй. Проверка: `check wip board`. `move ID in-progress` для третьей истории завершается с кодом 1 и строкой FAIL AGILE-6.

Не делать: переводить points в часы. Не ставить done без `gate done`.

Ready: `gate ready ID` требует родителя, points 1–8, сценарий и границы.

## epics

Ответственность: PO и BMAD lead. Код: `src/mazu_method/workflows.py` функция epic_tree_issues.

Делать: идея, эпик с родителем-идеей, истории с родителем-эпиком. Команда: `workflow epics --idea IDEA-001 --epic EPIC-001`.

Не делать: эпик на отдел. Историю на 13 и выше не проводить через ready, её режут.

## sprint

Ответственность: scrum master. Код: sprint_plan_issues.

Делать: `sprint new --goal "одна фраза"`, `sprint add --id US-001 --sprint S1`, затем `workflow sprint --sprint S1` и `gate sprint S1`.

Не делать: пустую цель и истории, которые не проходят ready.

Velocity печатает только points историй этого спринта в статусе done. Часы в эту сумму не входят.

Канбан: спринт не создают, двигают `move`, следят за `check wip board`.

## estimation

Ответственность: PO ставит points, разработчик пишет часы. Код: `src/mazu_method/estimation.py`.

Points только 1, 2, 3, 5, 8, 13, 21. Иное CLI не запишет. 13 и 21 не проходят ready.

Часы: `log ID 1.5 --note "..."`. `check points ID` печатает оба числа рядом и не складывает их.

Не делать: копировать одно число в оба поля и называть это оценкой.

## sysl

Ответственность: Sysl modeler. Код: `src/mazu_method/sysl_check.py`.

Делать: файл с блоком приложения, эндпоинтом на `/` и `return ... <: type`. Проверка: `check sysl diagrams/sysl/example.sysl`.

Не делать: класть пароли и ключи. Не считать картинку источником. Если программы рисования нет, так и сказать.

Примеры, которые уже проходят проверку: `diagrams/sysl/example.sysl` и `diagrams/sysl/backlog.sysl`.

## calm

Ответственность: CALM modeler. Код: `src/mazu_method/calm_check.py`.

Делать: JSON с nodes и relationships. У узла unique-id и node-type. Связь interacts или connects, source и destination существуют. Проверка: `check calm diagrams/calm/example.calm.json`.

Не делать: менять unique-id из-за подписи. Не описывать этим файлом поведение эндпоинта: для этого Sysl.

Примеры: `diagrams/calm/example.calm.json` и `diagrams/calm/backlog.calm.json`.

## architecture

Ответственность: председатель зовёт один из трёх уровней. Код поведения и состава — проверки Sysl и CALM, дорогой выбор — ADR.

Бизнес-архитектор пишет способности и не-цели. Энтерпрайз-архитектор пишет, кто владеет данными. Архитектор решения пишет контракт на этот спринт.

Не делать: один рисунок, где способности, границы систем и классы смешаны. Это остановка BOUND-2.

## dev

Ответственность: разработчик до review, ленивый сеньор решает, какой код не писать.

Делать: одну историю, `log`, лестницу из `skills/lazy-senior`. В конце ответа назвать, что не смотрели.

Не делать: ставить done, добавлять зависимость без guard, срезать проверку на границе доверия.

## gates

`gate ready ID` не двигает карточку. Он говорит, можно ли считать историю готовой.

`gate done ID` требует всё то же плюс улику на каждый сценарий.

`gate sprint ID` требует цель и ready у каждой истории спринта.

`check wip board` цель `board` здесь служебная: команда смотрит все истории, слово board не ищет карточку.

Код выхода 0 значит PASS. Иначе FAIL и ненулевой код. Агент не говорит «готово», если код не ноль.

## tools

`python3 cli/mazu.py tools` печатает команду, владельца и гейт.

Полный перечень методов в коде:

- bmad.py — фазы
- sdd.py — Always, Ask First, Never
- bdd.py — сценарии
- adr.py — файл решения
- agile.py — ready, done, лимит, velocity
- estimation.py — points и часы
- workflows.py — create-epics-and-stories и sprint-planning
- sysl_check.py — поведение
- calm_check.py — состав

Скачивание и первый запуск: `python3 cli/mazu.py doctor`, затем `python3 cli/mazu.py init`, затем команды этой страницы. Данные проекта остаются в `mazu-data/` и в репозиторий метода не коммитятся.
