#!/usr/bin/env python3
"""
Основной скрипт для демонстрации работы с облачной интеграцией
Задание №10: Интеграция с облачными сервисами
"""

import os
import sys
import json
from pathlib import Path
from colorama import Fore, Style, init
from github_cloud_manager import GitHubCloudManager

init(autoreset=True)


def print_header(title: str):
    """Печать заголовка"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Style.RESET_ALL}")


def print_success(message: str):
    """Печать сообщения о успехе"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str):
    """Печать сообщения о ошибке"""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_info(message: str):
    """Печать информационного сообщения"""
    print(f"{Fore.YELLOW}ℹ {message}{Style.RESET_ALL}")


def setup_demo_data():
    """Создание демо-данных для тестирования"""
    """Основные данные для тестирования"""
    demo_dir = "demo_data"
    os.makedirs(demo_dir, exist_ok=True)
    
    # Сохраняем тестовые файлы
    files = {
        "config.json": {
            "app_name": "Cloud Integration Demo",
            "version": "1.0.0",
            "backup_enabled": True,
            "auto_backup_interval": 3600
        },
        "data.txt": "This is test data for cloud backup.\nLine 2: Multiple lines supported.\nLine 3: All content will be backed up.",
        "README.md": "# Demo Data\n\nThis directory contains test files for cloud backup demonstration.\n\n## Files:\n- config.json: Configuration settings\n- data.txt: Sample text data"
    }
    
    for filename, content in files.items():
        filepath = os.path.join(demo_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            if isinstance(content, dict):
                json.dump(content, f, indent=2, ensure_ascii=False)
            else:
                f.write(content)
        print_success(f"Создан файл: {filepath}")
    
    # Создаем подпапку
    subdir = os.path.join(demo_dir, "subfolder")
    os.makedirs(subdir, exist_ok=True)
    
    with open(os.path.join(subdir, "nested.txt"), 'w', encoding='utf-8') as f:
        f.write("This is a nested file in a subdirectory.\nIt will be backed up preserving the folder structure.")
    
    print_success(f"Создана подпапка с файлом: {subdir}")
    
    return demo_dir


def demonstrate_single_file_operations(manager: GitHubCloudManager):
    """Демонстрация операций с ютим файлом"""
    print_header("1. ОПЕРАЦИИ С ОДИНОЧНЫМИ ФАЙЛАМИ")
    
    test_file = "demo_data/config.json"
    cloud_file = "single_files/config_backup.json"
    
    # Загрузка файла
    print_info("Загружаю файл в облако...")
    success, message = manager.upload_file(test_file, cloud_file, "Initial upload")
    if success:
        print_success(message)
    else:
        print_error(message)
    
    # Получение информации о файлах
    print_info("Получаю список файлов в облаке...")
    files = manager.list_files()
    if files:
        print_success(f"Найдено {len(files)} файлов:")
        for f in files[:5]:  # Показываем первые 5
            print(f"  - {f['name']} ({f['type']})")
    else:
        print_error("Файлы не найдены")
    
    # Скачивание файла
    print_info("Скачиваю файл из облака...")
    restore_file = "restored_single/config.json"
    success, message = manager.download_file(cloud_file, restore_file)
    if success:
        print_success(message)
        # Проверяем содержимое
        with open(restore_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print_info(f"Содержимое: {content[:100]}...")
    else:
        print_error(message)


def demonstrate_backup_restore(manager: GitHubCloudManager):
    """Демонстрация резервного копирования и восстановления"""
    print_header("2. РЕЗЕРВНОЕ КОПИРОВАНИЕ И ВОССТАНОВЛЕНИЕ")
    
    # Резервное копирование
    print_info("Начинаю резервное копирование директории...")
    backup_result = manager.backup_directory("demo_data", "backups/full_backup_v1")
    
    if backup_result["success"]:
        print_success(backup_result["message"])
        print_info(f"Размер резервной копии: {backup_result['total_size'] / 1024:.2f} KB")
        print_info(f"Файлов загружено: {backup_result['files_uploaded']}")
    else:
        print_error(backup_result["message"])
    
    # Получение списка резервных копий
    print_info("\nПолучаю список доступных резервных копий...")
    backups = manager.list_backups()
    if backups:
        print_success(f"Найдено {len(backups)} резервных копий:")
        for backup in backups:
            print(f"  - {backup['name']} (путь: {backup['path']})")
    else:
        print_info("Резервные копии не найдены")
    
    # Восстановление из резервной копии
    print_info("\nНачинаю восстановление из резервной копии...")
    restore_result = manager.restore_backup("backups/full_backup_v1", "restored_data")
    
    if restore_result["success"]:
        print_success(restore_result["message"])
        print_info(f"Файлов восстановлено: {restore_result['files_restored']}")
    else:
        print_error(restore_result["message"])
    
    # Проверяем восстановленные файлы
    if os.path.exists("restored_data"):
        print_info("Проверяю восстановленные файлы...")
        for root, dirs, files in os.walk("restored_data"):
            for file in files:
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                print(f"  ✓ {filepath} ({size} bytes)")


def demonstrate_repository_info(manager: GitHubCloudManager):
    """Демонстрация информации о репозитории"""
    print_header("3. ИНФОРМАЦИЯ О ОБЛАЧНОМ ХРАНИЛИЩЕ")
    
    info = manager.get_repo_info()
    if info:
        print_success("Информация о репозитории:")
        print(f"  Имя: {info['name']}")
        print(f"  URL: {info['url']}")
        print(f"  Описание: {info['description']}")
        print(f"  Приватный: {info['private']}")
        print(f"  Создан: {info['created_at']}")
        print(f"  Размер: {info['size']} KB")
    else:
        print_error("Не удалось получить информацию о репозитории")


def cleanup_demo_data():
    """Очистка демо-данных (опционально)"""
    import shutil
    dirs_to_remove = ["demo_data", "restored_data", "restored_single"]
    
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print_info(f"Удалена директория: {dir_path}")


def main():
    """Основная функция"""
    print_header("ДЕМОНСТРАЦИЯ: Интеграция с облачными сервисами (GitHub)")
    print(f"{Fore.CYAN}Задание №10 - Cloud Integration with GitHub{Style.RESET_ALL}")
    
    try:
        # Инициализация менеджера GitHub
        print_info("Инициализирую менеджер GitHub...")
        manager = GitHubCloudManager()
        print_success("Менеджер инициализирован успешно")
        
        # Инициализация или получение репозитория
        repo_name = "cloud-backup-demo"
        print_info(f"Инициализирую репозиторий '{repo_name}'...")
        if manager.initialize_backup_repo(repo_name):
            print_success(f"Репозиторий готов к использованию")
        else:
            print_error("Не удалось инициализировать репозиторий")
            return
        
        # Подготовка демо-данных
        print_header("ПОДГОТОВКА ДЕМО-ДАННЫХ")
        demo_dir = setup_demo_data()
        print_success(f"Демо-данные подготовлены в директории: {demo_dir}")
        
        # Демонстрация операций
        demonstrate_single_file_operations(manager)
        demonstrate_backup_restore(manager)
        demonstrate_repository_info(manager)
        
        # Итоговая статистика
        print_header("ИТОГОВАЯ СТАТИСТИКА")
        files_list = manager.list_files()
        backups_list = manager.list_backups()
        print_success(f"Всего файлов в облаке: {len(files_list)}")
        print_success(f"Всего резервных копий: {len(backups_list)}")
        
        print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print(f"{Fore.GREEN}✓ Успешно продемонстрированы:")
        print("  1. Загрузка файлов в облако")
        print("  2. Скачивание файлов из облака")
        print("  3. Резервное копирование директорий")
        print("  4. Восстановление данных из резервной копии")
        print(f"  5. Получение информации о облачном хранилище{Style.RESET_ALL}")
        
        # Вопрос об очистке
        response = input(f"\n{Fore.YELLOW}Удалить локальные демо-файлы? (y/n): {Style.RESET_ALL}").strip().lower()
        if response == 'y':
            cleanup_demo_data()
            print_success("Демо-файлы удалены")
        
    except KeyboardInterrupt:
        print_error("\nПрограмма прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print_error(f"Непредвиденная ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
