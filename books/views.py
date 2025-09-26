from rest_framework import mixins, viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from django.db.models import Count
from rest_framework.response import Response

from .models import Publisher, Book, Author

from .serializers import DetailPublisherSerializer, BookSerializer, AuthorDetailSerializer


class BookCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-published_date'


class BookPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100



class BooksAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # pagination_class = BookCursorPagination



class AuthorsAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer


class PublisherAPIView(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = DetailPublisherSerializer

    filter_backends = (filters.SearchFilter, filters.OrderingFilter)

    search_fields = ('name', )
    ordering_fields = ('name', '-established_date')

    @action(detail=False, methods=['GET'])
    def statistics(self, request):
        res = Publisher.objects.annotate(books_count=Count('books'))

        data = [
            {
                'id': item.pk,
                'name': item.name,
                'count': item.books_count
            }
            for item in res
        ]

        return Response(data, status=status.HTTP_200_OK)


