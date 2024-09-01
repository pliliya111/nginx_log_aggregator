from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from log_parser.models import NginxLog
from log_parser.serializers import NginxLogSerializer


class NginxLogPagination(PageNumberPagination):
    """
    Класс пагинации для логов Nginx.

    Этот класс определяет параметры пагинации для представления логов Nginx.

    Атрибуты:
    - page_size (int): Количество элементов на странице по умолчанию. Установлено в 10.
    - page_size_query_param (str): Параметр запроса, который позволяет клиенту
      указывать желаемый размер страницы. Установлено в "page_size".
    - max_page_size (int): Максимально допустимый размер страницы. Установлено в 100.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class LogParserAPIView(generics.ListAPIView):
    """
    Представление для получения списка логов Nginx.

    Это представление позволяет клиентам получать список логов Nginx с
    поддержкой пагинации и поиска.

    Атрибуты:
    - queryset: Определяет набор данных, который будет использоваться для
      получения логов Nginx. В данном случае это все объекты модели NginxLog.
    - serializer_class: Указывает, что для сериализации данных будет использоваться
      сериализатор NginxLogSerializer.
    - pagination_class: Указывает, что для пагинации будет использоваться
      класс NginxLogPagination.
    - filter_backends: Определяет, какие фильтры будут применяться к запросам.
      В данном случае используется SearchFilter для поддержки поиска.
    - search_fields: Указывает, по каким полям можно выполнять поиск.
      В данном случае это поля "ip_address", "http_method" и "uri".
    """

    queryset = NginxLog.objects.all()
    serializer_class = NginxLogSerializer
    pagination_class = NginxLogPagination
    filter_backends = (SearchFilter,)
    search_fields = ["ip_address", "http_method", "uri"]
