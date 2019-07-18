
properties = "firstName lastName dob email phone university specialization city state projects".split()


def get_team_json_from_array(person_array):
    person_json = {}

    currentIndex = 0

    for prop in properties:
        person_json[prop] = person_array[currentIndex]
        currentIndex += 1

    return person_json