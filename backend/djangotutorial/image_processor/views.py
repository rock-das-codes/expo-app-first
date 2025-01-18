from rest_framework.permissions import AllowAny

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from gradio_client import Client, handle_file

import shutil

from django.conf import settings

from django.core.files.uploadedfile import InMemoryUploadedFile

import os

from tempfile import NamedTemporaryFile

class ProcessImageView(APIView):

 permission_classes = [AllowAny]

 def post(self, request, *args, **kwargs):

   try:

     image = request.FILES.get("image")

     prompt = request.data.get("prompt")
     with NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

     client = Client("lllyasviel/iclight-v2")

     result = client.predict(

     input_fg=handle_file(temp_file.name),

     bg_source="None",

     prompt=prompt,

     image_width=896,

     image_height=1152,

     num_samples=1,

     seed=1345,

     steps=25,

     n_prompt="",

     cfg=1,

     gs=5,

     rs=1,

     init_denoise=0.999,

     api_name="/process")
     with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(result.get("image"))
            image_path = temp_file.name
     filename="processed_image.png"

     return Response({"result": result, "image_path": image_path}, status=status.HTTP_200_OK)

   except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)