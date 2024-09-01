from rest_framework.serializers import ModelSerializer
from log_parser.models import NginxLog

class NginxLogSerializer(ModelSerializer):
    """
    Сериализатор для модели NginxLog.

    Этот сериализатор используется для преобразования экземпляров модели
    NginxLog в JSON-формат и обратно. Он позволяет легко работать с данными
    модели в API.

    Атрибуты:
    - Meta: Вложенный класс, который определяет метаданные для сериализатора.
        - model: Указывает, что сериализатор связан с моделью NginxLog.
        - fields: Указывает, какие поля модели будут включены в сериализацию.
                  В данном случае используется "__all__", что означает,
                  что будут включены все поля модели.
    """

    class Meta:
        model = NginxLog
        fields = "__all__"
