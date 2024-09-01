from django.db import models

class NginxLog(models.Model):
    """
    Модель для хранения логов Nginx.

    Атрибуты:
    - ip_address (GenericIPAddressField): IP-адрес клиента, который сделал запрос.
    - date (DateTimeField): Дата и время, когда был сделан запрос.
    - http_method (CharField): HTTP-метод запроса (например, GET, POST).
    - uri (TextField): URI, к которому был сделан запрос.
    - response_code (IntegerField): Код ответа сервера (например, 200, 404).
    - response_size (BigIntegerField): Размер ответа в байтах.

    Методы:
    - __str__(): Возвращает строковое представление объекта в формате:
      "IP-адрес - Дата и время - HTTP-метод URI".
    """

    ip_address = models.GenericIPAddressField()
    date = models.DateTimeField()
    http_method = models.CharField(max_length=10)
    uri = models.TextField()
    response_code = models.IntegerField()
    response_size = models.BigIntegerField()

    def __str__(self):
        return f"{self.ip_address} - {self.date} - {self.http_method} {self.uri}"
