from django.core.paginator import Paginator
from django.db import connection, transaction, OperationalError


class TimeLimitedPaginator(Paginator):
    def count(self):
        with transaction.atomic(), connection.cursor() as cursor:
            cursor.execute('SET LOCAL statement_timeout TO 500;')
            try:
                return super().count
            except OperationalError:
                return 9999999999
