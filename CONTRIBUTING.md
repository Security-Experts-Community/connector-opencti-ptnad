# 🤝 Руководство по внесению вклада

Спасибо, что вы решили внести свой вклад в этот проект! Мы ценим ваше участие и стремимся сделать процесс внесения изменений максимально простым и понятным.

## Как внести свой вклад

### Начало работы

1. Убедитесь, что у вас установлены все необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Сделайте форк репозитория и клонируйте его локально:
   ```bash
   git clone https://github.com/Security-Experts-Community/connector-opencti-ptnad.git
   cd connector-opencti-ptnad
   ```

3. Добавьте оригинальный репозиторий как upstream:
   ```bash
   git remote add upstream https://github.com/Security-Experts-Community/connector-opencti-ptnad.git
   ```

### Процесс внесения изменений

- Создайте issue для обсуждения вашей идеи или исправления ошибки перед отправкой pull request.
- Сделайте форк репозитория и создайте свою ветку от `main`:
  ```bash
  git checkout -b feature/your-feature-name
  ```
- Пишите понятные и лаконичные сообщения коммитов, следуя [Conventional Commits](https://www.conventionalcommits.org/).
- Добавляйте тесты для новых функций или исправлений ошибок, если это возможно.
- Отправьте pull request и опишите ваши изменения.

### Шаблоны

При создании issue используйте соответствующие шаблоны:
- [Шаблон для сообщения об ошибках](https://github.com/Security-Experts-Community/connector-opencti-ptnad/issues/new?template=form_for_bugs.yml)
- [Шаблон для предложения улучшений](https://github.com/Security-Experts-Community/connector-opencti-ptnad/issues/new?template=form_for_features.yml)

## Кодекс поведения

Этот проект следует [Кодексу поведения](https://github.com/Security-Experts-Community/connector-opencti-ptnad?tab=coc-ov-file). Пожалуйста, будьте уважительны во всех взаимодействиях.

## Сообщение об ошибках

### Перед созданием issue

1. Проверьте существующие issues перед созданием нового.
2. Убедитесь, что ошибка воспроизводится в последней версии проекта.
3. Свертесь с документацией.

### Создание issue

При создании issue, пожалуйста, опишите:
- Четкое описание проблемы
- Шаги для воспроизведения проблемы
- Скриншоты
- Информацию об окружении:
  - Версия Python
  - Версия OpenCTI
  - Версия PT NAD
  - Операционная система

## Предложение улучшений

### Процесс

1. Объясните, почему улучшение будет полезным.
2. Предоставьте примеры, если это возможно.
3. Опишите, как это улучшение может быть реализовано.
4. Укажите, готовы ли вы помочь с реализацией.

### Типы улучшений

- Новые функции
- Улучшение документации
- Исправления ошибок

---
Если у вас есть вопросы, создайте [issue](https://github.com/Security-Experts-Community/connector-opencti-ptnad/issues) или свяжитесь с нами.