# Интеграция с облачными сервисами (GitHub)

## Задание № 10: Овладение способами сохранения и обработки данных в облачных системах.

---

## Цель работы

Освоить способы сохранения и обработки данных в облачных системах, демонстрируя работу с GitHub API для резервного копирования и восстановления.

---

## Основные понятия

### 1. Cloud Storage (GitHub API)
GitHub провайдирует REST API для работы с репозиториями а репозиториями как облачном схранилище.

### 2. SDK Integration (PyGithub)
PyGithub - это Python-библиотека для работы с GitHub API, обеспечивающая доступ к репозиториям и файлам.

### 3. Backup & Restore
- **Backup**: Нагрузка файлов и директорий в облак
- **Restore**: Овосстановление данных из облака

---

## Шаг 1: Регистрация в GitHub

### 1.1 Создание аккаунта
- Перейти на [github.com](https://github.com)
- Кликните "Sign up"
- Введите email, пароль и пользовательское имя

### 1.2 Настройка GitHub Personal Access Token

1. Найдите: **Settings** → **Developer settings** → **Personal access tokens**
2. Кликните **Generate new token (classic)**
3. Где мся права, выберите:
   - ✅ **repo** (full control of private repositories)
   - ✅ **read:user** 
 n   - ✅ **user:email**
4. Нанимая вы бережно удержите токен в безопасности

---

## Шаг 2: Настройка подключения к облаку

### 2.1 инсталляция зависимостей

```bash
# Клонируем репозиторий
git clone https://github.com/yourusername/Cloud-Integration-Backup-System.git
cd Cloud-Integration-Backup-System

# Устанавливаем пакеты
pip install -r requirements.txt
```

### 2.2 Настройка .env файла

```bash
# Скопируем шаблон
cp .env.example .env

# Открываем файл в оредакторе
vim .env  # или используйте на вас редактор
```

**Вставьте ваш GitHub token:**

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Шаг 3: демонстрация возможностей

### 3.1 Загружка и скачивание файлов

```python
from github_cloud_manager import GitHubCloudManager

# Инициализация
manager = GitHubCloudManager()

# Оинициализация репозитория
manager.initialize_backup_repo("my-backup-repo")

# Загружка файла
success, message = manager.upload_file(
    "local_file.txt",
    "cloud/remote_file.txt",
    "Initial upload"
)

# Скачивание файла
success, message = manager.download_file(
    "cloud/remote_file.txt",
    "restored_file.txt"
)
```

### 3.2 Резервное копирование

```python
# Резервное копирование директории
backup_result = manager.backup_directory(
    "./my_data",
    "backups/daily_backup"
)

print(f"Success: {backup_result['success']}")
print(f"Files uploaded: {backup_result['files_uploaded']}")
print(f"Total size: {backup_result['total_size']} bytes")
```

### 3.3 Восстановление данных

```python
# Восстановление из резервной копии
restore_result = manager.restore_backup(
    "backups/daily_backup",
    "./restored_data"
)

print(f"Success: {restore_result['success']}")
print(f"Files restored: {restore_result['files_restored']}")
```

### 3.4 Получение информации

```python
# Получение о облакном схранилище
repo_info = manager.get_repo_info()
print(f"Repository: {repo_info['name']}")
print(f"URL: {repo_info['url']}")
print(f"Size: {repo_info['size']} KB")

# Получение списка резервных копий
backups = manager.list_backups()
for backup in backups:
    print(f"- {backup['name']}: {backup['path']}")
```

---

## Запуск демонстрации

```bash
# Полная демонстрация
python main.py

# Или используйте конкретные операции
python -c "from github_cloud_manager import GitHubCloudManager; m = GitHubCloudManager(); m.initialize_backup_repo('test')"
```

---

## Материалы в репозитории

- **github_cloud_manager.py** - основной модуль на Python
- **main.py** - демонстрационный скрипт
- **requirements.txt** - зависимости Python
- **.env.example** - шаблон конфигурации
- **INSTRUCTIONS.md** - этот файл

---

## Основные возможности

✅ **Загружка файлов**
- Передача в облако
- Обновление вености цых в облаке

✅ **Скачивание файлов**
- Мастер веностя из облака
- Локальное сохранение

✅ **Резервное копирование**
- Понадиректорий
- Нарушение структуры
- Отслеживание размеров

✅ **Восстановление данных**
- Полное восстановление архивов
- Сохранение кструктуры темплатов
- Отмотка ошибок

✅ **Отслеживание**
- Йолбрес ни временные метки
- Аналитика реавка

---

## Контрольные вопросы

**Q: Нокое ограничение по размеру файлов?**
A: GitHub API чид максимум ~100 MB пер реквестованные загружки.

**Q: Как часто до резервные копии жертжа?**
A: Нерю можо настроить в .env (в секунд).

**Q: Как основное хранятя токены?**
A: Письма где токены не ваот в git - используйте .env и адд .env в .gitignore.

---

## Литература

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Cloud Storage Best Practices](https://cloud.google.com/docs/storing-data)

---

## Лицензия

MIT License
