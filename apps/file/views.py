from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from .models import File
from service.upload import Upload
from  .serializer import FileSerializer
from .permission import IsAuthenticated, IsClientUser, IsOperationUser
from base64 import b64encode
from config import settings
class FileViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]

    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method=='POST':
            return [IsOperationUser()]
        else:
            return [IsClientUser()]
    

    def create(self, request):
        
        file = request.FILES.get('file')
        if not file:
            return Response({"message":"file is required"}, status=status.HTTP_400_BAD_REQUEST)
                
        name = request.data.get('file_name', file.name)
        extension =file.name.split('.')[-1].lower()
        size=file.size

        description = request.data.get('description','')
        
        if extension not in ['xlsx','pptx','docx','doc']:
            return Response({"message":"file extension not supported"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uploaded_file = File.objects.create(name=name,description=description,extension=extension,size=size)
            temp_path = f'{settings.BASE_DIR}/tmp/{uploaded_file.id}_{file.name}'
            with open(temp_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            Upload.upload_file.delay(temp_path=temp_path,file_name=name,file_id=uploaded_file.id)
            return Response({'id': uploaded_file.id,"message":"File will be uploaded shortly"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

      
    
    def list(self, request):
        try:
            queryset = File.objects.filter().order_by('-uploaded_at')
            serializer = FileSerializer(queryset, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path="download") 
    def get_download_url(self, request):
        file_id = request.query_params.get("file_id")  

        if not file_id:
            return Response({"error": "file_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            res = Upload.get_signed_url(file)
            return Response(res, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
