from drf_yasg.utils import swagger_auto_schema

from django.utils import timezone
from rest_framework import mixins, viewsets, status, filters, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from django.db.models import Count
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .models import Publisher, Book, Author

from .serializers import DetailPublisherSerializer, BookSerializer, AuthorDetailSerializer


from rest_framework.permissions import BasePermission, DjangoModelPermissions


class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        curr_time = timezone.now()
        return 8 <= curr_time.time().hour <= 16 and (obj.owner == request.user or request.user.is_staff)

class BookCursorPagination(CursorPagination):

    page_size = 5
    ordering = '-published_date'


class BookPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class CanPublishAuthorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('can_publish_author')


class BookListCreateViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [DjangoModelPermissions, CanPublishAuthorPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_queryset(self):
    #     return Book.objects.filter(owner=self.request.user)

#
#
# #
# # @extend_schema(
# #     summary="Список книг",
# #     description="Возвращает список всех книг. Можно использовать пагинацию.",
# #     responses=BookSerializer(many=True),
# # )
# # class BooksAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
# #     # authentication_classes = [BasicAuthentication]
# #     queryset = Book.objects.all()
# #     serializer_class = BookSerializer
# #     # pagination_class = BookCursorPagination
#
#
#
# @extend_schema(
#     summary='Список авторов',
#     description='Возвращает список всех авторов',
#     responses=AuthorDetailSerializer(many=True),
# )
# class AuthorsAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
#     queryset = Author.objects.all()
#     serializer_class = AuthorDetailSerializer
#
#
# @extend_schema(
#     summary="CRUD издателей",
#     description="Полный CRUD для издателей. Можно искать и сортировать по имени и дате основания.",
#     responses=DetailPublisherSerializer(many=True),
#     parameters=[
#         OpenApiParameter(name='search', description='Поиск по имени издателя', required=False, type=str),
#         OpenApiParameter(name='ordering', description='Сортировка: name или -established_date', required=False, type=str),
#     ]
# )
# class PublisherAPIView(viewsets.ModelViewSet):
#     queryset = Publisher.objects.all()
#     serializer_class = DetailPublisherSerializer
#
#     filter_backends = (filters.SearchFilter, filters.OrderingFilter)
#
#     search_fields = ('name', )
#     ordering_fields = ('name', '-established_date')
#
#     @extend_schema(
#         summary="Статистика по книгам издателей",
#         description="Возвращает список издателей с количеством книг у каждого.",
#         responses=OpenApiResponse(
#             response=OpenApiResponse(
#                 description="Список издателей с количеством книг",
#                 examples=[
#                     {
#                         'id': 1,
#                         'name': 'Издательство А',
#                         'count': 10
#                     },
#                     {
#                         'id': 2,
#                         'name': 'Издательство Б',
#                         'count': 5
#                     },
#                 ]
#             )
#         ),
#     )
#     @action(detail=False, methods=['GET'])
#     def statistics(self, request):
#         res = Publisher.objects.annotate(books_count=Count('books'))
#
#         data = [
#             {
#                 'id': item.pk,
#                 'name': item.name,
#                 'count': item.books_count
#             }
#             for item in res
#         ]
#
#         return Response(data, status=status.HTTP_200_OK)
#

