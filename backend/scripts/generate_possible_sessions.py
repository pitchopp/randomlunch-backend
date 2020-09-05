from backend.models import Person, PossibleSession, PossibleCouple


def all_pairs(lst):
    if len(lst) < 2:
        yield []
        return
    if len(lst) % 2 == 1:
        # Handle odd length list
        for i in range(len(lst)):
            for result in all_pairs(lst[:i] + lst[i+1:]):
                yield result
    else:
        a = lst[0]
        for i in range(1,len(lst)):
            pair = (a,lst[i])
            for rest in all_pairs(lst[1:i]+lst[i+1:]):
                yield [pair] + rest


def is_session_valid(session):
    for couple in session:
        person_1 = couple[0]
        person_2 = couple[1]
        if not Person.test_persons_can_meet(person_1, person_2):
            return False
    return True


def save_session(session):
    ps = PossibleSession()
    ps.save()
    try:
        for couple in session:
            person_1 = couple[0]
            person_2 = couple[1]
            PossibleCouple(person_1=person_1, person_2=person_2, session=ps).save()
    except Exception as e:
        ps.delete()
        print("session saving failed with : " + str(e))


def run():
    persons = list(Person.objects.filter(active=True))
    combinations = all_pairs(persons)
    PossibleSession.objects.all().delete()
    for session in combinations:
        if is_session_valid(session):
            save_session(session)
