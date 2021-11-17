from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([])
def signup(request):
    data = {'data': '', 'status': ''}
    user_serializer = UserSerializer(data=request.data)

    if user_serializer.is_valid():
        user_serializer.save()

        data['data'] = {
            'user':
                {
                    'email': user_serializer.data.get('email'),
                    'username': user_serializer.data.get('username'),
                },
            'token': Token.objects.get(user__username=user_serializer.data.get('username')).key,
            'message': 'Created'
        }
        data['status'] = status.HTTP_201_CREATED
    else:
        data['data'] = user_serializer.errors
        data['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**data)


@api_view(['DELETE'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(data="user is logout", status=status.HTTP_200_OK)