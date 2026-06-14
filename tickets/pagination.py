from rest_framework.pagination import PageNumberPagination

class MoivPagintion(PageNumberPagination):
  page_size = 10
  page_query_param = "page_size"
  max_page_size = 100