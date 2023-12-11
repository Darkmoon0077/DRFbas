from time import sleep
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import File
from .forms import ContactForm
from django.http import HttpResponse
from .serializers import FileUploadSerializer
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError

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

@shared_task
def keksend(form_data):
    form = ContactForm(form_data)
    if form.is_valid():
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['from_email']
        message = form.cleaned_data['message']
    try:
        send_mail('JJJ', 'kkk', None, ['Darkmoon077@yandex.kz'], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Ошибка в теме письма.')

@shared_task
def brend():
    try:
        send_mail('Аида', 'Я люблю теб...... водку, я имел ввиду водку', 'darkmoon0077@gmail.com', ['aida.raimbekova@narxoz.kz'], fail_silently=False)
        return {'status': 'success', 'message': 'Email sent successfully!'}
    except Exception as e:
        return {'status': 'error', 'message': f'Email was not sent successfully! Error: {e}'}