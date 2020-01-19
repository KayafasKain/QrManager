from rest_framework import serializers

from .validators import validation_rules, validate_colors
from .models import QrCode, QrStats


class QrCodeSerializer(serializers.ModelSerializer):
    background_color = serializers.CharField(
        max_length=16,
        validators=[validate_colors],
    )
    foreground_color = serializers.CharField(
        max_length=16,
        validators=[validate_colors],
    )

    def is_valid(self, raise_exception=False):
        if super().is_valid(raise_exception):
            code_type = self.initial_data['code_type']
            payload = self.initial_data['payload']

            if not validation_rules[code_type].match(payload):
                raise serializers.ValidationError(
                    'Payload does not matches specified type',
                )

    class Meta:
        model = QrCode
        fields = [
            'payload', 'name', 'slug', 'code_type',
            'foreground_color', 'background_color',
            'created_at', 'updated_at', 'id',
        ]


class QrStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrStats
        fields = ['ip', 'browser', 'qr_code']


class QrScanSerializer(serializers.ModelSerializer):
    total_scans = serializers.IntegerField(default=0)
    unique_scans = serializers.IntegerField(default=0)

    class Meta:
        model = QrCode
        fields = [
            'payload', 'name', 'code_type', 'total_scans', 'slug',
            'background_color', 'foreground_color', 'unique_scans',
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

