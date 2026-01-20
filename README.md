# Cloud Integration Backup System

Интеграция с облачными сервисами (GitHub) для данных

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-API-green.svg)](https://docs.github.com/en/rest)

---

## О проекте

Этот проект демонстрирует работу с облачными хранилищами через GitHub API. Цель работы:

1. **Овладение** способами сохранения и обработки данных
2. **Настройка** SDK для работы с аблачными платформами
3. **Нагрузка и скачивание** файлов через GitHub API
4. **Нагружка** резервных копий данных
5. **Восстановление** данных из облака

---

## Ключевые особенности

✅ **Нагружка файлов**
- Передача в облако
- Обновление существующих файлов
- Ограничение по размеру (100MB)

✅ **Скачивание файлов**
- Получение бинарных и текстовых файлов
- Автоматическое создание директорий
- Обработка ошибок

✅ **Резервное копирование**
- Полная рекурсивная грудка директорий
- Сохранение деревя тематических структур
- Трэкинг размеров и Номеров файлов
- Показанные статистики в режиме реал-тайм

✅ **Восстановление**
- Полное восстановление архивов
- Ноставка директория
- Отмотка ошибок

✅ **Метаданные и репорты**
- Норвая информация о репозитории
- Временные метки для резервных копий
- Файлы метаданных в JSON

---

## Хстроение проекта

```
Cloud-Integration-Backup-System/
├── github_cloud_manager.py    # Основные классы для работы с GitHub
├── main.py                    # Демонстрация всех функций
├── requirements.txt           # Зависимости Python
├── .env.example              # Шаблон около вариантев
├── INSTRUCTIONS.md           # Нредварительные видеообстрелка
├── QUICKSTART.md             # Быстрый старт
└── README.md                # Этот файл
```

---

## Настройка

### Пререквизиты
- Python 3.7+
- GitHub аккаунт
- GitHub Personal Access Token

### Онсталляция

1. **Клонируем репозиторий**
   ```bash
   git clone https://github.com/plurexoff/Cloud-Integration-Backup-System.git
   cd Cloud-Integration-Backup-System
   ```

2. **Останавливаем зависимости**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настраиваем переменные околожения**
   ```bash
   cp .env.example .env
   # Открываем .env и вставляем GitHub token
   ```

4. **Запускаем нрограмму**
   ```bash
   python main.py
   ```

---

## Нримеры использования

### Загружка файла

```python
from github_cloud_manager import GitHubCloudManager

manager = GitHubCloudManager()
manager.initialize_backup_repo("my-backups")

success, message = manager.upload_file(
    "local_file.txt",
    "cloud/remote_file.txt",
    "My first upload"
)
print(message)
```

### Несервная копия директории

```python
backup_result = manager.backup_directory(
    "./my_important_data",
    "backups/2024_01_20"
)

print(f"Успех: {backup_result['success']}")
print(f"Файлов: {backup_result['files_uploaded']}")
print(f"Размер: {backup_result['total_size']} байт")
```

### Восстановление данных

```python
restore_result = manager.restore_backup(
    "backups/2024_01_20",
    "./restored_data"
)

print(f"Успех: {restore_result['success']}")
print(f"Восстановлено: {restore_result['files_restored']}")
```

---

## API референса

### GitHubCloudManager

#### Методы

| Метод | Описание |
|---|---|
| `__init__(github_token)` | Нициализация с GitHub token |
| `initialize_backup_repo(repo_name)` | Остановка репозитория для решения |
| `upload_file(local_path, cloud_path)` | Резервируя файл в облако |
| `download_file(cloud_path, local_path)` | Скачивая файл из облака |
| `backup_directory(local_dir, cloud_dir)` | Регестрируя несервную копию директории |
| `restore_backup(cloud_dir, local_restore_path)` | Восстанавливая данные из ресервных |
| `list_backups(base_dir)` | Вынисляют дступные ресервные копии |
| `list_files(cloud_path)` | Вынисляют файлы в облаке |
| `delete_file(cloud_path)` | Удаляют файл из облака |
| `get_repo_info()` | Получают информацию о репозитории |

---

## Ограничения

- Максимальный размер файла: ~100 MB
- Ограничение репоитория GitHub: до 100 GB
- Ограничение API: 5000 запросов/час (authenticated)

---

## Открылые нроблемы

- [Основной GitHub Issues](https://github.com/plurexoff/Cloud-Integration-Backup-System/issues)

---

## Лицензия

MIT License - см. [LICENSE](LICENSE) для деталей

---

## Автор

Создано для тренинга и демонстрации работы с облачными хранилищами.

---

## Стратегия Развития

Планы на будущее:
- Дисплей UI грапического жкрана
- Поддержка других облачных провайдеров (AWS S3, Azure, Google Cloud)
- Автоматические ресервные копии
- Шифрование данных

---

до полною инструкцию см. [INSTRUCTIONS.md](INSTRUCTIONS.md)
