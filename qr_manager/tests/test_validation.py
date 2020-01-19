from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from ..models import QrCode


class QrValidationTestCases(APITestCase):
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

    def test_qr_code_invalid_color(self):
        data = {
          "payload": "Test Plain Text!",
          "name": "Super Name",
          "slug": "test-create",
          "code_type": "plain_text",
          "foreground_color": "#fcba.,.jk,g%03",
          "background_color": "#іві%324154",
        }

        responses = [
            self.client.post('/api/code/', data, format='json'),
            self.client.patch(
                '/api/code/%s/' % self.preset_code_id, data, format='json',
            ),
            self.client.put(
                '/api/code/%s/' % self.preset_code_id, data, format='json',
            ),
        ]
        for response in responses:
            self.assertEqual(
                response.data,
                {
                    'foreground_color': [
                        ErrorDetail(
                            string='Please, provide color in HEX format',
                            code='invalid',
                        ),
                    ],
                    'background_color': [
                        ErrorDetail(
                            string='Please, provide color in HEX format',
                            code='invalid',
                        ),
                    ],
                },
            )

    def test_qr_code_invalid_payload(self):
        data = {
          "payload": "Test Plain Text!",
          "name": "Super Name",
          "slug": "test-create",
          "code_type": "href",
          "foreground_color": "#1111111",
          "background_color": "#0000000",
        }

        responses = [
            self.client.post('/api/code/', data, format='json'),
            self.client.patch(
                '/api/code/%s/' % self.preset_code_id, data, format='json',
            ),
            self.client.put(
                '/api/code/%s/' % self.preset_code_id, data, format='json',
            ),
        ]
        for response in responses:
            self.assertEqual(
                response.data,
                [
                    ErrorDetail(
                        string='Payload does not matches specified type',
                        code='invalid',
                    ),
                ],
            )
