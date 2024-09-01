from rest_framework import status
from rest_framework.test import APITestCase
from .models import NginxLog

class NginxLogTests(APITestCase):
    def setUp(self):
        self.log = NginxLog.objects.create(
            ip_address='79.136.114.202',
            date='2015-06-04T10:06:52+03:00',
            http_method='GET',
            uri='/downloads/product_1',
            response_code=200,
            response_size=490
        )

    def test_get_logs(self):
        response = self.client.get('/api/v1/logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_log_detail(self):
        response = self.client.get(f'/api/v1/logs/{self.log.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ip_address'], self.log.ip_address)
