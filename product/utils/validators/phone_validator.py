from django.core.validators import _lazy_re_compile, RegexValidator


validate_phone = RegexValidator(
    _lazy_re_compile(r'^(998+[0-9]{9})$'),
    message='invalid correct phone number',
    code='-1005',
)
