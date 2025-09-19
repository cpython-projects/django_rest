from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Book, BookAuthor, Author, Publisher
from .serializers import ListOfPublisherSerializer, DetailPublisherSerializer, CreatePublisherSerializer
from .serializers import BookListSerializer, BookSerializer, AuthorDetailSerializer



class BookListView(APIView, PageNumberPagination):
    page_size = 5

    def get(self, request):
        books = Book.objects.all()
        self.page_size = self.get_page_size(request)
        result = self.paginate_queryset(books, request, view=self)


        serializer = BookListSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size', None)
        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size


    # def get(self, request):
    #
    #     # items_for_filter = ['year', 'author', 'publisher']
    #
    #     filters = {}
    #
    #     # for key, value in request.query_params.items():
    #     #     if key in items_for_filter:
    #     #         filters[key] = value
    #
    #     year = request.query_params.get('year', None)
    #     is_bestseller = request.query_params.get('is_bestseller', None)
    #
    #
    #     sort_by = request.query_params.get('sort_by', 'title')
    #     sort_order = request.query_params.get('sort_order', 'asc')
    #     sort_order = '-' if sort_order == 'desc' else ''
    #
    #     if year is not None:
    #         filters['published_date__year'] = year
    #
    #     if is_bestseller is not None:
    #         filters['is_bestseller'] = is_bestseller
    #
    #     res = Book.objects.filter(**filters).order_by(f'{sort_order}{sort_by}')
    #
    #     serializer = BookListSerializer(res, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)










# class AuthorListView(generics.ListAPIView):
#     queryset = Author.objects.all()
#
#     def get_serializer_class(self):
#         return AuthorDetailSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer





class CreateListBookView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializer
        return BookSerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



@api_view(['GET', 'POST'])
def mybooks(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'POST'])
def publishers(request):
    if request.method == 'GET':
        publishers_collection = Publisher.objects.all()
        serializer = ListOfPublisherSerializer(publishers_collection, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = CreatePublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def publisher_detail(request, pk):
    try:
        publisher = Publisher.objects.get(pk=pk)
    except Publisher.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DetailPublisherSerializer(publisher)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CreatePublisherSerializer(publisher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        publisher.delete()
        return Response({"message": "Deleted success"}, status=status.HTTP_204_NO_CONTENT)