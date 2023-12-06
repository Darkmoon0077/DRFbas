from time import sleep
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import File
from .serializers import FileUploadSerializer
from celery import shared_task

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            upload_file.delay(file.id)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

@shared_task
def upload_file(file_id):
    try:
        file = File.objects.get(id=file_id)
        sleep(7) 
        print(f"File with ID {file_id} processed successfully.")
    except File.DoesNotExist:
        print(f"File with ID {file_id} not found.")
