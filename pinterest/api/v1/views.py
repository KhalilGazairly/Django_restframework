from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from pinterest.models import Movie
from .serializers import MovieSerializer

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission


class UserCanDeleteMovie(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='CanDelete').exists():
            return True
        return False


@api_view(['GET'])
@permission_classes([IsAdminUser])
def hello(request):
    data= {'message from rest api'}
    return Response(data=data)


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serialized_movies = MovieSerializer(instance=movies, many=True)
    return Response(data=serialized_movies.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def movie_details(request, pk):
    try:
        movie_obj = Movie.objects.get(pk=pk)

    except Exception as e:
        return Response(data={'message':'failed Movie dose not exist'}, status=status.HTTP_400_BAD_REQUEST)

    serialized_movies = MovieSerializer(instance=movie_obj)
    return Response(data=serialized_movies.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def movie_create(request):
    serialized_movies = MovieSerializer(data=request.data)
    if serialized_movies.is_valid():
        serialized_movies.save()
    else:
        return Response(data=serialized_movies.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=serialized_movies.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([UserCanDeleteMovie])
def movie_delete(request, pk):
    response = {}
    try:
        movie_obj = Movie.objects.get(pk=pk)
        movie_obj.delete()
        response['data']= {'message': 'Successfully Deleted Movie'}
        response['status'] = status.HTTP_200_OK
    except Exception as e:
        response['data'] = {'message': 'Error while Deleting {}'.format(str(e))}
        response['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**response)


@api_view(['PUT', 'PATCH'])
def movie_update(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)

    except Exception as e:
        return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serialized_movies = MovieSerializer(instance=movie, data=request.data)
    elif request.method == 'PATCH':
        serialized_movies = MovieSerializer(instance=movie, data=request.data, partial=True)

    if serialized_movies.is_valid():
        serialized_movies.save()
        return Response(data=serialized_movies.data, status=status.HTTP_200_OK)

    return Response(data=serialized_movies.errors, status=status.HTTP_400_BAD_REQUEST)
