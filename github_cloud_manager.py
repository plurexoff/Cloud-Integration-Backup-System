#!/usr/bin/env python3
"""
GitHub Cloud Manager - интеграция с облачными сервисами GitHub
Модуль для управления файлами через GitHub API
"""

import os
import json
import base64
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from github import Github, GithubException, InputGitTreeElement
from dotenv import load_dotenv
from colorama import Fore, Style, init
from tqdm import tqdm
import hashlib

# Инициализация colorama для цветного вывода
init(autoreset=True)

# Загрузка переменных окружения
load_dotenv()


class GitHubCloudManager:
    """Класс для управления облачными хранилищами через GitHub API"""

    def __init__(self, github_token: Optional[str] = None):
        """
        Инициализация менеджера GitHub
        
        Args:
            github_token: GitHub Personal Access Token (если None, берется из переменных окружения)
        """
        token = github_token or os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError(
                "GitHub token not found. Set GITHUB_TOKEN environment variable or pass it as argument"
            )
        
        self.github = Github(token)
        self.user = self.github.get_user()
        self.repo = None
        self.backup_metadata = {}
        
    def initialize_backup_repo(self, repo_name: str) -> bool:
        """
        Инициализация или получение репозитория для резервных копий
        
        Args:
            repo_name: Имя репозитория для резервных копий
            
        Returns:
            True если успешно инициализирован, False иначе
        """
        try:
            # Попытаемся получить существующий репозиторий
            self.repo = self.user.get_repo(repo_name)
            print(f"{Fore.GREEN}✓ Репозиторий '{repo_name}' найден{Style.RESET_ALL}")
            return True
        except GithubException:
            print(f"{Fore.YELLOW}! Репозиторий '{repo_name}' не найден, создаю...{Style.RESET_ALL}")
            try:
                self.repo = self.user.create_repo(
                    name=repo_name,
                    description="Cloud Backup System - GitHub Cloud Integration",
                    private=True,
                    auto_init=True
                )
                print(f"{Fore.GREEN}✓ Репозиторий '{repo_name}' успешно создан{Style.RESET_ALL}")
                return True
            except GithubException as e:
                print(f"{Fore.RED}✗ Ошибка при создании репозитория: {str(e)}{Style.RESET_ALL}")
                return False
    
    def upload_file(self, local_path: str, cloud_path: str, message: str = None) -> Tuple[bool, str]:
        """
        Загрузка файла в облако (GitHub)
        
        Args:
            local_path: Путь к локальному файлу
            cloud_path: Путь в репозитории GitHub
            message: Сообщение коммита
            
        Returns:
            Кортеж (успех, сообщение)
        """
        if not self.repo:
            return False, "Репозиторий не инициализирован"
        
        if not os.path.exists(local_path):
            return False, f"Локальный файл не найден: {local_path}"
        
        try:
            with open(local_path, 'rb') as f:
                content = f.read()
            
            file_size = len(content)
            if file_size > 100 * 1024 * 1024:  # 100MB
                return False, "Файл слишком большой (>100MB)"
            
            commit_message = message or f"Upload: {os.path.basename(local_path)}"
            
            # Проверяем существует ли файл
            try:
                existing_file = self.repo.get_contents(cloud_path)
                # Если файл существует, обновляем его
                self.repo.update_file(
                    path=cloud_path,
                    message=commit_message,
                    content=content,
                    sha=existing_file.sha
                )
                return True, f"Файл обновлен: {cloud_path}"
            except GithubException:
                # Если файл не существует, создаем его
                self.repo.create_file(
                    path=cloud_path,
                    message=commit_message,
                    content=content
                )
                return True, f"Файл загружен: {cloud_path}"
                
        except Exception as e:
            return False, f"Ошибка при загрузке: {str(e)}"
    
    def download_file(self, cloud_path: str, local_path: str) -> Tuple[bool, str]:
        """
        Скачивание файла из облака (GitHub)
        
        Args:
            cloud_path: Путь файла в репозитории GitHub
            local_path: Путь для сохранения локального файла
            
        Returns:
            Кортеж (успех, сообщение)
        """
        if not self.repo:
            return False, "Репозиторий не инициализирован"
        
        try:
            file_content = self.repo.get_contents(cloud_path)
            content = file_content.decoded_content
            
            # Создаем директории если их нет
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            with open(local_path, 'wb') as f:
                f.write(content)
            
            return True, f"Файл скачан: {local_path}"
            
        except GithubException as e:
            return False, f"Файл не найден в облаке: {cloud_path}"
        except Exception as e:
            return False, f"Ошибка при скачивании: {str(e)}"
    
    def backup_directory(self, local_dir: str, cloud_dir: str = "backups") -> Dict[str, any]:
        """
        Резервное копирование директории
        
        Args:
            local_dir: Локальная директория для резервной копии
            cloud_dir: Директория в облаке для хранения резервной копии
            
        Returns:
            Словарь с результатами резервной копии
        """
        if not self.repo:
            return {"success": False, "message": "Репозиторий не инициализирован"}
        
        if not os.path.isdir(local_dir):
            return {"success": False, "message": f"Директория не найдена: {local_dir}"}
        
        backup_info = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "source_dir": local_dir,
            "cloud_dir": cloud_dir,
            "files_uploaded": 0,
            "files_failed": 0,
            "total_size": 0,
            "details": []
        }
        
        print(f"\n{Fore.CYAN}Начинаю резервное копирование: {local_dir}{Style.RESET_ALL}")
        
        # Сканируем все файлы в директории
        files_to_backup = []
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                file_path = os.path.join(root, file)
                files_to_backup.append(file_path)
        
        if not files_to_backup:
            backup_info["message"] = "Нет файлов для резервной копии"
            return backup_info
        
        # Загружаем файлы с прогресс-баром
        for file_path in tqdm(files_to_backup, desc="Загрузка файлов"):
            relative_path = os.path.relpath(file_path, os.path.dirname(local_dir))
            cloud_path = f"{cloud_dir}/{relative_path.replace(chr(92), '/')}"
            
            file_size = os.path.getsize(file_path)
            backup_info["total_size"] += file_size
            
            success, message = self.upload_file(
                file_path,
                cloud_path,
                f"Backup: {relative_path}"
            )
            
            if success:
                backup_info["files_uploaded"] += 1
                backup_info["details"].append({
                    "file": relative_path,
                    "size": file_size,
                    "status": "success"
                })
            else:
                backup_info["files_failed"] += 1
                backup_info["details"].append({
                    "file": relative_path,
                    "error": message,
                    "status": "failed"
                })
        
        backup_info["success"] = backup_info["files_failed"] == 0
        backup_info["message"] = f"Загружено {backup_info['files_uploaded']} файлов, ошибок: {backup_info['files_failed']}"
        
        # Сохраняем метаданные резервной копии
        self._save_backup_metadata(backup_info, cloud_dir)
        
        return backup_info
    
    def restore_backup(self, cloud_dir: str, local_restore_path: str) -> Dict[str, any]:
        """
        Восстановление из резервной копии
        
        Args:
            cloud_dir: Директория в облаке содержащая резервную копию
            local_restore_path: Локальный путь для восстановления
            
        Returns:
            Словарь с результатами восстановления
        """
        if not self.repo:
            return {"success": False, "message": "Репозиторий не инициализирован"}
        
        restore_info = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "cloud_dir": cloud_dir,
            "restore_path": local_restore_path,
            "files_restored": 0,
            "files_failed": 0,
            "details": []
        }
        
        print(f"\n{Fore.CYAN}Начинаю восстановление из: {cloud_dir}{Style.RESET_ALL}")
        
        try:
            # Получаем список файлов в облаке
            contents = self.repo.get_contents(cloud_dir)
            files_to_restore = self._get_all_files(contents)
            
            if not files_to_restore:
                restore_info["message"] = "Нет файлов для восстановления"
                return restore_info
            
            os.makedirs(local_restore_path, exist_ok=True)
            
            # Скачиваем файлы с прогресс-баром
            for file_obj in tqdm(files_to_restore, desc="Скачивание файлов"):
                relative_path = file_obj.path.replace(f"{cloud_dir}/", "")
                local_file_path = os.path.join(local_restore_path, relative_path.replace('/', chr(92)))
                
                success, message = self.download_file(file_obj.path, local_file_path)
                
                if success:
                    restore_info["files_restored"] += 1
                    restore_info["details"].append({
                        "file": relative_path,
                        "status": "success"
                    })
                else:
                    restore_info["files_failed"] += 1
                    restore_info["details"].append({
                        "file": relative_path,
                        "error": message,
                        "status": "failed"
                    })
            
            restore_info["success"] = restore_info["files_failed"] == 0
            restore_info["message"] = f"Восстановлено {restore_info['files_restored']} файлов, ошибок: {restore_info['files_failed']}"
            
        except GithubException as e:
            restore_info["message"] = f"Директория не найдена в облаке: {cloud_dir}"
        except Exception as e:
            restore_info["message"] = f"Ошибка при восстановлении: {str(e)}"
        
        return restore_info
    
    def list_backups(self, base_dir: str = "backups") -> List[Dict]:
        """
        Получение списка доступных резервных копий
        
        Args:
            base_dir: Базовая директория для поиска резервных копий
            
        Returns:
            Список резервных копий
        """
        if not self.repo:
            return []
        
        try:
            contents = self.repo.get_contents(base_dir)
            
            if not isinstance(contents, list):
                contents = [contents]
            
            backups = []
            for item in contents:
                if item.type == "dir":
                    backups.append({
                        "name": item.name,
                        "path": item.path,
                        "created": item.created_at.isoformat() if hasattr(item, 'created_at') else "Unknown"
                    })
            
            return backups
        except GithubException:
            return []
    
    def list_files(self, cloud_path: str = "") -> List[Dict]:
        """
        Получение списка файлов в облаке
        
        Args:
            cloud_path: Путь в облаке
            
        Returns:
            Список файлов
        """
        if not self.repo:
            return []
        
        try:
            if cloud_path:
                contents = self.repo.get_contents(cloud_path)
            else:
                contents = self.repo.get_contents("")
            
            if not isinstance(contents, list):
                contents = [contents]
            
            files = []
            for item in contents:
                files.append({
                    "name": item.name,
                    "path": item.path,
                    "type": item.type,
                    "size": item.size if hasattr(item, 'size') else 0
                })
            
            return files
        except GithubException as e:
            print(f"{Fore.RED}✗ Ошибка при получении списка файлов: {str(e)}{Style.RESET_ALL}")
            return []
    
    def delete_file(self, cloud_path: str) -> Tuple[bool, str]:
        """
        Удаление файла из облака
        
        Args:
            cloud_path: Путь файла в облаке
            
        Returns:
            Кортеж (успех, сообщение)
        """
        if not self.repo:
            return False, "Репозиторий не инициализирован"
        
        try:
            file_content = self.repo.get_contents(cloud_path)
            self.repo.delete_file(
                path=cloud_path,
                message=f"Delete: {os.path.basename(cloud_path)}",
                sha=file_content.sha
            )
            return True, f"Файл удален: {cloud_path}"
        except GithubException as e:
            return False, f"Ошибка при удалении: {str(e)}"
    
    def _get_all_files(self, contents, files: List = None):
        """
        Рекурсивно получить все файлы из содержимого
        
        Args:
            contents: Содержимое репозитория
            files: Список файлов
            
        Returns:
            Список всех файлов
        """
        if files is None:
            files = []
        
        if not isinstance(contents, list):
            contents = [contents]
        
        for item in contents:
            if item.type == "file":
                files.append(item)
            elif item.type == "dir":
                try:
                    sub_contents = self.repo.get_contents(item.path)
                    self._get_all_files(sub_contents, files)
                except GithubException:
                    pass
        
        return files
    
    def _save_backup_metadata(self, backup_info: Dict, cloud_dir: str):
        """
        Сохранение метаданных резервной копии
        
        Args:
            backup_info: Информация о резервной копии
            cloud_dir: Директория в облаке
        """
        metadata = {
            "backup_dir": cloud_dir,
            "timestamp": backup_info["timestamp"],
            "files_count": backup_info["files_uploaded"],
            "total_size": backup_info["total_size"],
            "status": "success" if backup_info["success"] else "partial"
        }
        
        metadata_path = f"{cloud_dir}/metadata.json"
        try:
            self.upload_file(
                None,  # Мы создаем файл напрямую
                metadata_path,
                "Update backup metadata"
            )
        except:
            pass  # Игнорируем ошибки при сохранении метаданных
    
    def get_repo_info(self) -> Dict:
        """
        Получение информации о репозитории
        
        Returns:
            Словарь с информацией о репозитории
        """
        if not self.repo:
            return {}
        
        return {
            "name": self.repo.name,
            "url": self.repo.html_url,
            "description": self.repo.description,
            "private": self.repo.private,
            "created_at": self.repo.created_at.isoformat(),
            "updated_at": self.repo.updated_at.isoformat(),
            "size": self.repo.size,
            "language": self.repo.language
        }


if __name__ == "__main__":
    print(f"{Fore.CYAN}GitHub Cloud Manager Module{Style.RESET_ALL}")
    print("Этот модуль предназначен для импорта в другие скрипты.")
