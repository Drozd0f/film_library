import math


class Paginator:
    _page = 1
    _limit = 10
    _total_pages = 0

    def __init__(self, page: str, limit: str):
        if page.isnumeric():
            page = int(page)
            if page > 1:
                self._page = page
        if limit.isnumeric():
            limit = int(limit)
            if limit > 100:
                self._limit = 100
            elif limit >= 1:
                self._limit = limit

    @property
    def page(self) -> int:
        return self._page

    @property
    def limit(self) -> int:
        return self._limit

    @property
    def total_pages(self) -> int:
        return self._total_pages

    @total_pages.setter
    def total_pages(self, total_count):
        self._total_pages = math.ceil(total_count / self.limit)

    def to_dict(self) -> dict:
        return {
            'page': self.page,
            'limit': self.limit,
            'total_pages': self.total_pages,
        }
