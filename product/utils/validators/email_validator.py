from django.core.validators import _lazy_re_compile, RegexValidator

validate_email = RegexValidator(
    _lazy_re_compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
    message='invalid correct email',
    code='-1005',
)

