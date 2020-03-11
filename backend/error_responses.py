from django.http import JsonResponse
from rest_framework import status


class ErrorResponses:
    @staticmethod
    def error_500(e: str = None) -> JsonResponse:
        return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def method_not_allowed(request) -> JsonResponse:
        return JsonResponse({"message": "method " + request.method + " not allowed"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
