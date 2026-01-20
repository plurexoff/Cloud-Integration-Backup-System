#!/usr/bin/env python3
"""
Полезные примеры использования GitHubCloudManager
"""

from github_cloud_manager import GitHubCloudManager
import os
from datetime import datetime


def example_1_basic_file_operations():
    """Пример 1: Основные операции с файлами"""
    print("\n=== Пример 1: Основные операции ===")
    
    try:
        # Инициализируем менеджер
        manager = GitHubCloudManager()
        print("[+] Менеджер готов")
        
        # Остановка репозитория
        if manager.initialize_backup_repo("cloud-demo"):
            print("[+] Репозиторий готов")
        
        # Тестовые данные
        test_file = "test_example.txt"
        with open(test_file, 'w') as f:
            f.write("Ныъ Это тестовый файл \n Test content")
        
        # Выгружаем в облак
        success, msg = manager.upload_file(test_file, "examples/test.txt")
        print(f"[+] Загружка: {msg}")
        
        # Скачиваем обратно
        success, msg = manager.download_file("examples/test.txt", "test_restored.txt")
        print(f"[+] Скачивание: {msg}")
        
        # Очистка
        os.remove(test_file)
        os.remove("test_restored.txt")
        
    except Exception as e:
        print(f"[-] Ошибка: {e}")


def example_2_backup_restore():
    """Пример 2: Ресервная копия и восстановление"""
    print("\n=== Пример 2: Ресервная копия ===")
    
    try:
        manager = GitHubCloudManager()
        manager.initialize_backup_repo("cloud-demo")
        
        # Создаем тестовую директорию
        os.makedirs("test_data", exist_ok=True)
        
        # Сохраняем тестовые файлы
        for i in range(3):
            with open(f"test_data/file_{i}.txt", 'w') as f:
                f.write(f"Content of file {i}")
        
        # Начинаем ресервную копию
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_result = manager.backup_directory(
            "test_data",
            f"backups/example_{timestamp}"
        )
        
        print(f"[+] Резервная копия: {backup_result['message']}")
        print(f"    Файлов загружено: {backup_result['files_uploaded']}")
        print(f"    Размер: {backup_result['total_size']} байт")
        
        # Восстанавливаем
        restore_result = manager.restore_backup(
            f"backups/example_{timestamp}",
            "test_data_restored"
        )
        
        print(f"[+] Восстановление: {restore_result['message']}")
        print(f"    Файлов восстановлено: {restore_result['files_restored']}")
        
        # Очистка
        import shutil
        shutil.rmtree("test_data")
        shutil.rmtree("test_data_restored")
        
    except Exception as e:
        print(f"[-] Ошибка: {e}")


def example_3_list_and_info():
    """Пример 3: Списки и информация"""
    print("\n=== Пример 3: Списки и информация ===")
    
    try:
        manager = GitHubCloudManager()
        manager.initialize_backup_repo("cloud-demo")
        
        # Получаем информацию о репозитории
        repo_info = manager.get_repo_info()
        print("[+] Информация о репозитории:")
        print(f"    Имя: {repo_info.get('name')}")
        print(f"    URL: {repo_info.get('url')}")
        print(f"    Описание: {repo_info.get('description')}")
        print(f"    Размер: {repo_info.get('size')} KB")
        
        # Получаем список файлов
        files = manager.list_files()
        print(f"\n[+] Файлы в облаке ({len(files)} всего):")
        for f in files[:10]:  # Покажем первые 10
            print(f"    - {f['name']} ({f['type']})")
        
        # Получаем ресервные копии
        backups = manager.list_backups()
        print(f"\n[+] Ресервные копии ({len(backups)} всего):")
        for backup in backups:
            print(f"    - {backup['name']}")
        
    except Exception as e:
        print(f"[-] Ошибка: {e}")


def example_4_error_handling():
    """Пример 4: Обработка ошибок"""
    print("\n=== Пример 4: Обработка ошибок ===")
    
    try:
        manager = GitHubCloudManager()
        manager.initialize_backup_repo("cloud-demo")
        
        # Попытка загружить несуществующий файл
        success, message = manager.upload_file(
            "non_existent_file.txt",
            "cloud/file.txt"
        )
        print(f"[–] Результат: {message}")
        
        # Попытка скачать несуществующий файл
        success, message = manager.download_file(
            "non_existent_cloud_file.txt",
            "local_file.txt"
        )
        print(f"[–] Результат: {message}")
        
        # Попытка скачать несуществующую директорию
        result = manager.restore_backup(
            "non_existent_backup",
            "restored_data"
        )
        print(f"[–] Результат: {result['message']}")
        
    except Exception as e:
        print(f"[-] Ошибка: {e}")


if __name__ == "__main__":
    print("Гитхаб Cloud Manager - Примеры")
    print("="*50)
    
    # Запуските выбранные примеры
    try:
        example_1_basic_file_operations()
        example_2_backup_restore()
        example_3_list_and_info()
        example_4_error_handling()
    except KeyboardInterrupt:
        print("\n[–] Прервано пользователем")
    
    print("\n" + "="*50)
    print("Примеры выполнены")
