from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def test_view ( request):
    print(request)
    return Response({'data':'test api'})

