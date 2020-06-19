import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend.error_responses import ErrorResponses
from backend.models import Person, Session, Couple
from backend.serializers import PersonSerializer, SessionSerializer
from randomlunch.randomsession import get_random_couples


def persons(request):
    try:
        if request.method == 'GET':
            response = JsonResponse(PersonSerializer(Person.objects.all(), many=True).data, safe=False)
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            return response
        else:
            return ErrorResponses.method_not_allowed(request)
    except Exception as e:
        return ErrorResponses.error_500(str(e))


def sessions(request):
    try:
        if request.method == 'GET':
            return JsonResponse(SessionSerializer(Session.objects.filter(valid=True), many=True).data, safe=False)
        else:
            return ErrorResponses.method_not_allowed(request)
    except Exception as e:
        return ErrorResponses.error_500(str(e))


@csrf_exempt
def random_session(request):
    #try:
    if request.method == 'POST':
        session = Session()
        session.save()
        list_persons = list(Person.objects.all())
        couples = get_random_couples(list_persons)
        for couple in couples:
            Couple(
                session=session,
                person_1=couple[0],
                person_2=couple[1]
            ).save()
        time.sleep(4)
        return JsonResponse(SessionSerializer(session).data, safe=False)
    else:
        return ErrorResponses.method_not_allowed(request)
    #except Exception as e:
    #    return ErrorResponses.error_500(str(e))


@csrf_exempt
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


@csrf_exempt
def sessions(request):
    try:
        if request.method == 'GET':
            valid_sessions = Session.objects.filter(valid=True)
            return JsonResponse(SessionSerializer(valid_sessions, many=True).data, safe=False)
        else:
            return ErrorResponses.method_not_allowed(request)
    except Exception as e:
        return ErrorResponses.error_500(str(e))
