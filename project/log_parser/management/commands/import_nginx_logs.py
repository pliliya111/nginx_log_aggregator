import logging
import os
from datetime import datetime
import requests
from django.core.management.base import BaseCommand
from log_parser.models import NginxLog

# Настройка логирования
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
    Команда для импорта логов Nginx из указанного URL или локального файла.

    Аргументы:
        source (str): URL файла логов или путь к локальному файлу.
    """

    help = "Import Nginx logs from a given URL or local file"

    def add_arguments(self, parser):
        """
        Добавляет аргументы командной строки для команды.

        Аргументы:
            parser (ArgumentParser): Парсер аргументов командной строки.
        """
        parser.add_argument(
            "source", type=str, help="URL of the log file or path to local file"
        )

    def handle(self, *args, **kwargs):
        """
        Обрабатывает команду, загружая логи из указанного источника.

        Аргументы:
            *args: Необязательные позиционные аргументы.
            **kwargs: Необязательные именованные аргументы, включая 'source'.
        """
        source = kwargs["source"]

        # Проверка, является ли источник URL
        if source.startswith("http://") or source.startswith("https://"):
            response = requests.get(source, stream=True)
            if response.status_code != 200:
                logger.error(f"Failed to fetch log file: {response.status_code}")
                return
            lines = response.iter_lines()
        else:
            # Проверка, является ли источник локальным файлом
            if not os.path.isfile(source):
                logger.error(f"Local file does not exist: {source}")
                return
            with open(source, "r") as file:
                lines = file.readlines()
        log_entries = []
        for line in lines:
            if line:
                log_entry = self.parse_line(
                    line.decode("utf-8") if isinstance(line, bytes) else line
                )
                if log_entry:
                    log_entries.append(log_entry)
        batch_size = 1000
        for i in range(0, len(log_entries), batch_size):
            NginxLog.objects.bulk_create(log_entries[i:i + batch_size])

    def parse_line(self, line):
        """
        Парсит строку лога и сохраняет данные в базе данных.

        Аргументы:
            line (str): Строка лога для парсинга.
        """
        import json

        try:
            # Предполагается, что строка лога в формате JSON
            log_entry = json.loads(line)
            ip_address = log_entry.get("remote_ip")
            date_str = log_entry.get("time")
            http_method, uri, _ = log_entry.get("request").split()
            response_code = log_entry.get("response")
            response_size = log_entry.get("bytes")

            # Преобразование строки даты в объект datetime
            date = datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S %z")
            return NginxLog(
                ip_address=ip_address,
                date=date,
                http_method=http_method,
                uri=uri,
                response_code=response_code,
                response_size=response_size,
            )
        except (json.JSONDecodeError, ValueError) as e:
            # Логирование предупреждения в случае ошибки парсинга
            logger.warning(f"Skipping invalid log line: {line} - Error: {e}")
            return None
