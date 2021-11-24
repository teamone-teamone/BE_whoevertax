from rest_framework.views import APIView
from rest_framework import generics, serializers
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from user.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.contrib.auth import authenticate
# 모임 리스트 시리얼라이저. api에서 보여줄 필드 명시


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'nickname', 'date_joined')


# api/moim 으로 get하면 이 listview로 연결
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def list(self, request):
        print(request.user)
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


def checkUser(request):
    if request.user:
        print(request.user)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


class ExampleView(APIView):

    def get(self, request, format=None):
        content = {
            'user': request.user.nickname.__str__(),
        }
        return Response(content)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get('email')
    print(email)
    password = request.data.get('password')

    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

        # 여기서 authenticate로 유저 validate
    user = authenticate(email=email, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

        # user 로 토큰 발행
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_200_OK)
