from rest_framework import status
from rest_framework.test import APITestCase

from log_parser.models import NginxLog


class NginxLogTests(APITestCase):
    def setUp(self):
        for i in range(25):
            NginxLog.objects.create(
                ip_address=f"79.136.114.{i}",
                date="2015-06-04T10:06:52+03:00",
                http_method="GET",
                uri=f"/downloads/product_{i}",
                response_code=200,
                response_size=490,
            )

    def test_get_logs(self):
        # Проверка получения списка логов
        response = self.client.get("/api/v1/logs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    def test_pagination(self):
        # Проверка пагинации
        response = self.client.get("/api/v1/logs/?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])

        response = self.client.get("/api/v1/logs/?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])

        response = self.client.get("/api/v1/logs/?page=3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 5
        )  # Проверяем, что на третьей странице 5 записей
        self.assertIsNone(
            response.data["next"]
        )  # Проверяем, что нет следующей страницы

    def test_search_logs(self):
        response = self.client.get("/api/v1/logs/?search=79.136.114.0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
