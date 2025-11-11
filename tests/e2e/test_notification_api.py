import pytest
import requests
import time
from uuid import UUID
from datetime import datetime

BASE_URL = "http://localhost:8002/api/notifications"

class TestNotificationAPI:
    """Компонентные тесты для Notification Service API"""

    def test_health_check(self):
        """Проверка что сервис запустился и отвечает"""
        # Ждем пока сервис полностью запустится
        time.sleep(5)

        try:
            response = requests.get(f"{BASE_URL}/")
            # Ожидаем либо 200, либо 404 если список пустой, но сервис работает
            assert response.status_code in [200, 404]
        except requests.exceptions.ConnectionError:
            pytest.fail("Сервис не запустился или недоступен на порту 8002")

    def test_send_notification_success(self):
        """Тест успешной отправки уведомления"""
        notification_data = {
            "type": "booking_confirmed",
            "message": "Your booking has been confirmed",
            "recipient": "user@example.com"
        }

        response = requests.post(f"{BASE_URL}/", json=notification_data)

        assert response.status_code == 200
        data = response.json()

        # Проверяем структуру ответа
        assert "id" in data
        assert data["type"] == "booking_confirmed"
        assert data["message"] == "Your booking has been confirmed"
        assert data["recipient"] == "user@example.com"
        assert data["status"] == "sent"
        assert "created_at" in data

        # Проверяем что ID валидный UUID
        try:
            UUID(data["id"])
        except ValueError:
            pytest.fail("ID notification должен быть валидным UUID")

    def test_send_notification_without_recipient(self):
        """Тест отправки уведомления без получателя"""
        notification_data = {
            "type": "cleaning_done",
            "message": "Cleaning has been completed"
        }

        response = requests.post(f"{BASE_URL}/", json=notification_data)

        assert response.status_code == 200
        data = response.json()

        assert data["type"] == "cleaning_done"
        assert data["recipient"] is None
        assert data["status"] == "sent"

    def test_list_notifications(self):
        """Тест получения списка уведомлений"""
        response = requests.get(f"{BASE_URL}/")

        assert response.status_code == 200
        notifications = response.json()

        assert isinstance(notifications, list)

        # Если есть уведомления, проверяем их структуру
        if notifications:
            notification = notifications[0]
            assert "id" in notification
            assert "type" in notification
            assert "message" in notification
            assert "status" in notification
            assert "created_at" in notification

    def test_get_nonexistent_notification(self):
        """Тест получения несуществующего уведомления"""
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        response = requests.get(f"{BASE_URL}/{non_existent_id}")

        assert response.status_code == 404
        assert "detail" in response.json()

    def test_send_notification_all_types(self):
        """Тест отправки уведомлений всех типов"""
        notification_types = [
            "booking_confirmed", "booking_canceled", "order_placed",
            "cleaning_done", "shift_assigned", "shift_extended",
            "shift_shortened", "shift_reallocated", "review_rejected"
        ]

        for notification_type in notification_types:
            notification_data = {
                "type": notification_type,
                "message": f"Test message for {notification_type}",
                "recipient": "test@example.com"
            }

            response = requests.post(f"{BASE_URL}/", json=notification_data)
            assert response.status_code == 200
            assert response.json()["type"] == notification_type

    def test_notification_timestamp(self):
        """Тест что временная метка создается корректно"""
        notification_data = {
            "type": "shift_assigned",
            "message": "You have been assigned to a shift"
        }

        before_send = datetime.utcnow()
        response = requests.post(f"{BASE_URL}/", json=notification_data)
        after_send = datetime.utcnow()

        notification = response.json()
        created_at = datetime.fromisoformat(notification["created_at"].replace('Z', '+00:00'))

        # Проверяем что время создания между before_send и after_send
        assert before_send <= created_at <= after_send