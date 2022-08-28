from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _


def deposit_should_be_multiply_5(value):
    if value % 5 == 0:
        return value
    else:
        raise ValidationError(_("Should be multiply of 5"))
