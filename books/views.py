from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book, BookAuthor, Author, Publisher
from .serializers import ListOfPublisherSerializer, DetailPublisherSerializer, CreatePublisherSerializer
from .serializers import BookListSerializer


@api_view(['GET'])
def mybooks(request):

    books = Book.objects.all()
    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



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