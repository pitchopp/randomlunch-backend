import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from backend.error_responses import ErrorResponses
from backend.models import Person, Session, Couple, PossibleSession
from backend.serializers import PersonSerializer, SessionSerializer
from randomlunch.randomsession import get_random_couples


@api_view(['GET'])
def persons(request):
    try:
        if request.method == 'GET':
            return JsonResponse(PersonSerializer(Person.objects.filter(active=True), many=True).data, safe=False)
        else:
            return ErrorResponses.method_not_allowed(request)
    except Exception as e:
        return ErrorResponses.error_500(str(e))


@api_view(['GET'])
def sessions(request):
    try:
        if request.method == 'GET':
            return JsonResponse(SessionSerializer(Session.objects.filter(valid=True), many=True).data, safe=False)
        else:
            return ErrorResponses.method_not_allowed(request)
    except Exception as e:
        return ErrorResponses.error_500(str(e))


@api_view(['POST'])
def random_session(request):
    try:
        if request.method == 'POST':
            session = Session()
            session.save()
            rand_sess = PossibleSession.get_random()
            for couple in rand_sess.couples:
                Couple(
                    session=session,
                    person_1=couple.person_1,
                    person_2=couple.person_2
                ).save()
            time.sleep(4)
            return JsonResponse(SessionSerializer(session).data, safe=False)
        else:
            return ErrorResponses.method_not_allowed(request)
    except Exception as e:
       return ErrorResponses.error_500(str(e))


@api_view(['PUT'])
def validate_session(request, session_id):
    try:
        if request.method == 'PUT':
            session = Session.objects.get(pk=session_id)
            session.valid = True
            session.save()
            return JsonResponse(SessionSerializer(session).data, safe=False)
        else:
            return ErrorResponses.method_not_allowed(request)
    except Exception as e:
        return ErrorResponses.error_500(str(e))


@api_view(['GET'])
def sessions(request):
    try:
        if request.method == 'GET':
            valid_sessions = Session.objects.filter(valid=True)
            return JsonResponse(SessionSerializer(valid_sessions, many=True).data, safe=False)
        else:
            return ErrorResponses.method_not_allowed(request)
    except Exception as e:
        return ErrorResponses.error_500(str(e))
