# Быстрый старт

## Первые шаги (5 минут)

### 1. Настройка околожения

```bash
# Копируем шаблон
cp .env.example .env

# Открываем в редакторе и вставляем токен
echo 'GITHUB_TOKEN=your_token_here' >> .env
```

### 2. Установка абисимостей

```bash
pip install -r requirements.txt
```

### 3. Запуск программы

```bash
python main.py
```

---

## Учитываются требования

- Python 3.7+
- GitHub аккаунт
- GitHub Personal Access Token (repo scope)

---

## Простое использование

```python
from github_cloud_manager import GitHubCloudManager

# Нициализация
manager = GitHubCloudManager()
manager.initialize_backup_repo("my-backups")

# Загружка файла
manager.upload_file("myfile.txt", "cloud/myfile.txt")

# Резервная копия директории
manager.backup_directory("./data", "backups/v1")

# Восстановление
manager.restore_backup("backups/v1", "./restored")
```

---

## Где получить токен

1. Пойти на [github.com/settings/tokens](https://github.com/settings/tokens)
2. Нажать "Generate new token (classic)"
3. Выбрать оско репо
4. Копировать о вставить в .env

---

## Основные операции

| Операция | Метод |
|---|---|
| Загружка | `upload_file(local, cloud)` |
| Скачивание | `download_file(cloud, local)` |
| Резерв | `backup_directory(dir, cloud_dir)` |
| Восстановка | `restore_backup(cloud_dir, local)` |

---

## Ошибки?

✅ Проверьте GitHub token в .env
✅ Проверьте интернет-коннективность
✅ Проверьте вродные пометки гитхаб-токена

Открой full INSTRUCTIONS.md для большего руководства.
