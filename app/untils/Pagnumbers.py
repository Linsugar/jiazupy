from rest_framework.pagination import CursorPagination

class Pag(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 4
    ordering = 'id'


