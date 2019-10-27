from rest_framework import viewsets
from .models import Essay, Album, Files
from .serializers import EssaySerializer, AlbumSerializer, FilesSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
# 미디어 파일 = 사용자들이 직접 업로드 할 수 있는 사진,파일을 나타내는 모델들
class PostViewSet(viewsets.ModelViewSet):
    queryset=Essay.objects.all()
    serializer_class=EssaySerializer

    filter_backends = [SearchFilter]
    search_fields = ('title', 'body')

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

    # 현재 request 를 보낸 유저 
    # == self.request.user

    def get_queryset(self):
        qs = super().get_queryset()
        
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                qs=Essay.objects.all()
            else:
                qs = qs.filter(author = self.request.user)
        else:
            qs = qs.none()

        return qs

class ImgViewSet(viewsets.ModelViewSet):
    queryset=Album.objects.all()
    serializer_class=AlbumSerializer

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

        
class FileViewSet(viewsets.ModelViewSet):
    queryset=Files.objects.all()
    serializer_class=FilesSerializer
    parser_classes = (MultiPartParser, FormParser)
    # 파일을 업로드 할 때는 형식이 여러가지 이므로 다양한 미디어 형식을 등록할 수 있게 해줌

    # file 업로드 문제점 해결
    # parser_class 지정
    # create() 오버라이딩 - > post()
    # API HTTP -> get() post() http 를 오버라이딩 한 것과 유사

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)
    