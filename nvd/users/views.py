from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from nvd.users.models import CustomUser
from nvd.users.serializers import UserSerializer


@api_view(['GET'])
def list_users(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({"users": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    data = request.data
    try:
        user = CustomUser.objects.update_or_create(username=data['username'],
                                                   first_name=data['first_name'],
                                                   email=data['email'], role=data['role'],
                                                   is_active=True)
        user[0].set_password(data['password'])
        user[0].save()
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(user[0])
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        username = request.user.username
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"message": "Bad request."}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(user)
    return Response({"users": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    data = request.data
    username = request.user.username
    try:
        CustomUser.objects.filter(username=username).update(first_name=data['first_name'],
                                                            email=data['email'], role=data['role'])
        user = CustomUser.objects.get(username=username)
        user.set_password(data['password'])
        user.save()
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(user)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)
