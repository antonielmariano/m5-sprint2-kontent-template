from django.forms import model_to_dict
from rest_framework.views import APIView, Response, status, Request
from .models import Content
from .validators import Validator
import ipdb


class ContentView(APIView):
    def get(self, request: Request) -> Response:
        result = Content.objects.all()
        database = [model_to_dict(data) for data in result]
        return Response(database, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        result = Validator.is_valid(**request.data)
        if result[0] is True:
            data = Content.objects.create(**request.data)
            data_dict = model_to_dict(data)
            return Response(data_dict, status.HTTP_201_CREATED)

        return Response(result[1], status.HTTP_400_BAD_REQUEST)


class ContentDetailView(APIView):
    def get(self, request: Request, content_id) -> Response:
        try:
            result = Content.objects.get(id=content_id)
            data = model_to_dict(result)
            return Response(data, status.HTTP_200_OK)
        except Content.DoesNotExist:
            message = {"message": "Content not found."}
            return Response(message, status.HTTP_404_NOT_FOUND)

    def patch(self, request: Request, content_id) -> Response:
        try:
            result = Content.objects.get(id=content_id)
            for key, value in request.data.items():
                setattr(result, key, value)
            result.save()
            return Response(model_to_dict(result))
        except Content.DoesNotExist:
            message = {"message": "Content not found."}
            return Response(message, status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, content_id) -> Response:
        try:
            result = Content.objects.get(id=content_id)
            result.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Content.DoesNotExist:
            message = {"message": "Content not found."}
            return Response(message, status.HTTP_404_NOT_FOUND)


class ContentFilterView(APIView):
    def get(self, request: Request) -> Response:
        try:
            title = request.query_params.get('title')
            result = Content.objects.filter(title=title)

            if len(result) == 0:
                message = {"message": "Content not found."}
                return Response(message, status.HTTP_404_NOT_FOUND)

            filtered = [model_to_dict(data) for data in result]
            return Response(filtered, status.HTTP_200_OK)
        except Content.DoesNotExist:
            message = {"message": "Content not found."}
            return Response(message, status.HTTP_404_NOT_FOUND)
