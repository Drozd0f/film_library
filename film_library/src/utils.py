from datetime import date

from pydantic.datetime_parse import get_numeric, parse_date


class StrictDate(date):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_date

    @classmethod
    def validate_date(cls, v) -> date:
        if get_numeric(v, native_expected_type='%Y-%m-%d') is not None:
            raise ValueError('Don\'t allow numbers')
        return parse_date(v)
