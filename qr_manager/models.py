from django.db import models

CodeType = [
    ('plain_text', 'Text'),
    ('email', 'Email'),
    ('href', 'Link'),
]


class QrCode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payload = models.TextField()
    name = models.CharField(unique=False, max_length=32)
    slug = models.CharField(unique=True, max_length=64)
    code_type = models.CharField(
        choices=CodeType,
        max_length=100,
    )
    background_color = models.CharField(unique=False, max_length=16)
    foreground_color = models.CharField(unique=False, max_length=16)

    class Meta:
        ordering = ['updated_at']


class QrStats(models.Model):
    ip = models.CharField(max_length=16, unique=False)
    browser = models.CharField(
        null=True,
        unique=False,
        default=None,
        max_length=64,
    )
    qr_code = models.ForeignKey('QrCode', null=False, on_delete=models.CASCADE)
