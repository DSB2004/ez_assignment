from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = File
        fields = [
            'id','name','description','extension','size','uploaded_at' 
        ]
        read_only_fields = ['id']
        
