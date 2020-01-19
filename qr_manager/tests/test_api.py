from unittest.mock import ANY
from collections import OrderedDict

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import QrCode


class QrCRUDTestCases(APITestCase):
    def setUp(self):
        preset_code = QrCode(
          payload="Test Plain Text!",
          name="Preset Super Name",
          slug="super-qr-preset",
          code_type="plain_text",
          foreground_color="#fcba03",
          background_color="#3da154"
        )
        preset_code.save()

        self.preset_code_id = preset_code.pk

    def test_get_qr_code(self):
        response = self.client.get('/api/code/%s/' % self.preset_code_id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                'payload': 'Test Plain Text!',
                'name': 'Preset Super Name',
                'slug': 'super-qr-preset',
                'code_type': 'plain_text',
                'foreground_color': '#fcba03',
                'background_color': '#3da154',
                'created_at': ANY,
                'updated_at': ANY,
                'id': 1,
            }
        )

    def test_list_qr_code(self):
        response = self.client.get('/api/code/?page=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            OrderedDict([
                ('count', 1), ('next', None), ('previous', None),
                ('results', [
                    OrderedDict([
                        ('payload', 'Test Plain Text!'),
                        ('name', 'Preset Super Name'),
                        ('slug', 'super-qr-preset'),
                        ('code_type', 'plain_text'),
                        ('foreground_color', '#fcba03'),
                        ('background_color', '#3da154'),
                        ('created_at', ANY),
                        ('updated_at', ANY),
                        ('id', 1),
                    ]),
                ]),
            ]),
        )

    def test_create_qr_code(self):
        data = {
          "payload": "Test Plain Text!",
          "name": "Super Name",
          "slug": "test-create",
          "code_type": "plain_text",
          "foreground_color": "#fcba03",
          "background_color": "#3da154"
        }

        response = self.client.post('/api/code/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            QrCode.objects.get(slug='test-create').name,
            'Super Name',
        )

    def test_patch_qr_code(self):
        data = {
          "payload": "Test Plain Text!",
          "name": "New Super Name",
          "code_type": "plain_text",
          "foreground_color": "#fcba03",
          "background_color": "#3da154"
        }

        response = self.client.patch(
            '/api/code/%s/' % self.preset_code_id,
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            QrCode.objects.get(pk=self.preset_code_id).name,
            'New Super Name',
        )

    def test_put_qr_code(self):
        data = {
            "payload": "Test Plain Text!",
            "name": "New Super Name",
            "code_type": "plain_text",
            "slug": "new-slug",
            "foreground_color": "#fcba03",
            "background_color": "#3da154"
        }

        response = self.client.put(
            '/api/code/%s/' % self.preset_code_id,
            data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            QrCode.objects.get(pk=self.preset_code_id).name,
            'New Super Name',
        )
        self.assertEqual(
            QrCode.objects.get(pk=self.preset_code_id).slug,
            'new-slug',
        )

    def test_delete_qr_code(self):
        response = self.client.delete(
            '/api/code/%s/' % self.preset_code_id,
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
