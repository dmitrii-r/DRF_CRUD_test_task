from http import HTTPStatus

import pytest


@pytest.mark.django_db
class TestEndpointsAvailability:

    @pytest.mark.parametrize(
        'url, meaning', [
            ('/api/schema/', 'схемы'),
            ('/api/schema/swagger-ui/', 'Swagger представления'),
            ('/api/schema/redoc/', 'Redoc представления'),
        ]
    )
    def test_schema(self, url, meaning, client) -> None:
        """Производит тест доступности эндпоинтов drf_spectacular."""
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            f'Убедитесь, что эндпоинт получения {meaning} документации '
            f'функционирует и доступен по адресу "{url}".'
        )
        return
