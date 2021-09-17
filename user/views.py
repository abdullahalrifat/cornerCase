from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout as user_logout
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):

    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass

    user_logout(request)
    return Response({"success": "Successfully logged out."},
                    status=status.HTTP_200_OK)
