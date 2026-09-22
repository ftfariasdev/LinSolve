from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health(request):
    """Verifica se o backend está no ar."""
    return Response({'status': 'ok', 'message': 'Backend funcionando'})
