import re

from django.core.exceptions import ValidationError
from django.db import models


class TelPhoneField(models.CharField):
    description = 'A field for telPhone'

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs.keys():
            kwargs['max_length'] = 104
        if 'validators' not in kwargs.keys():
            kwargs['validators'] = []
        kwargs['validators'].append(TelPhoneField.tel_phone_validate)
        super().__init__(*args, **kwargs)

    @staticmethod
    def tel_phone_validate(value: str):
        if len(value) != 0:
            pattern = re.compile(r'^([0-9]{2}-[0-9]{11})$')
            is_match = re.match(pattern, value)
            if is_match is None:
                raise ValidationError("This is not valid tel-phone number, please input +XX-XXXXXXXXXXX.")
            else:
                return value


class GenderField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs.keys():
            kwargs['max_length'] = 20
        if 'choices' not in kwargs.keys():
            kwargs['choices'] = [
                (1, 'male'),
                (0, 'female')
            ]
        super().__init__(*args, **kwargs)


class AgeField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs.keys():
            kwargs['max_length'] = 20
        if 'validators' not in kwargs.keys():
            kwargs['validators'] = []
        kwargs['validators'].append(AgeField.age_validate)
        super().__init__(*args, **kwargs)

    @staticmethod
    def age_validate(value: int):
        if value is not None:
            if value < 0 or value > 150:
                raise ValidationError('Thisis not valid age input, please input 0 ~ 150.')


class EducationBackgroundField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs.keys():
            kwargs['max_length'] = 20
        if 'choices' not in kwargs.keys():
            kwargs['choices'] = [
                (0, 'undergraduate（本科）'),
                (1, 'junior（专科）'),
                (2, 'senior（高中）'),
                (3, 'junior（初中）'),
            ]
        super().__init__(*args, **kwargs)
