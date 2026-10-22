# Роли

Каждая роль — файл в `agents/`. Это инструкция агенту, не отдельный процесс.

| Роль | Файл | Граница |
|---|---|---|
| Analyst | analyst.md | не выбирает архитектуру |
| PO | po.md | не подменяет points часами |
| Architect | architect.md | не придумывает ценность |
| SM | scrum-master.md | не меняет принятый ADR |
| Dev | dev.md | не ставит done |
| QA | qa.md | не закрывает без улики |
| BMAD lead | bmad-lead.md | не перескакивает фазу |
| SDD author | sdd-author.md | не пишет реализацию до границ |
| BDD author | bdd-author.md | не прячет шаги реализации в Then |
| ADR keeper | adr-keeper.md | не удаляет старый ADR |
| Sysl modeler | sysl-modeler.md | не считает картинку источником |
| CALM modeler | calm-modeler.md | не кладёт секреты в узлы |
| Integrator | integrator.md | не объявляет синхронизацию без успешного pull |
| Skill creator | skill-creator.md | не копирует чужой репозиторий внутрь |
| Researcher | researcher.md | не выдумывает имя конфига |
| Writer | writer.md | не описывает команду, которой нет в `--help` |
| Release | release.md | не называет метод готовым без зелёного audit |

Четыре эксперта Grok перечислены в `agents/catalog.json`: BMAD, SDD, ADR, BDD. Остальные роли из таблицы агент исполняет по файлу, даже если отдельного бота с таким именем нет.
