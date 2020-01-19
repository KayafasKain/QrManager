import re
from rest_framework import serializers

validation_rules = {
    'href': re.compile('(https?:\/\/(?:))'),
    'plain_text': re.compile(''),
    'email': re.compile(
        'mailto:{\S+@\S+\.\S+}\?subject={\S+}\&body={\S+}',
    ),
}

color_rule = re.compile('^#[A-z0-9]+$')


def validate_colors(value):
    if not color_rule.match(value):
        raise serializers.ValidationError(
            'Please, provide color in HEX format',
        )
