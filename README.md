# Практическое задание №3: Память и подтверждение действий

## Requirements
- [high] Добавить зависимость langgraph: В файле зависимостей (requirements.txt или pyproject.toml) добавить строку pip install langgraph
- [high] Подключить библиотеку rich: Установить rich и импортировать Console для вывода сообщений
- [high] Заменить собственный MemorySaver: Удалить/заменить класс MemorySaver, импортировать MemorySaver из langgraph.checkpoint.memory и создать экземпляр memory = MemorySaver()
- [high] Передать чекпоинтер в create_agent: В вызове create_agent добавить аргумент checkpointer=memory
- [high] Настроить паузу перед инструментом: В create_agent добавить interrupt_before=['tools']
- [high] Обработать __interrupt__ в цикле stream: В функции ask_and_run при получении chunk_type 'updates' проверить наличие '__interrupt__' в chunk_data и state.next == ('tools',) для запроса подтверждения пользователя
- [high] Реализовать рекурсивный вызов ask_and_run при подтверждении: Если пользователь вводит 'Y', вызвать ask_and_run(None, config) для возобновления
- [high] Обновить чат‑цикл: В основном цикле использовать ask_and_run с config, где thread_id задаётся как 'разговор-1'
