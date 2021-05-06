import re
from .models import User

def validate(key, value):

    def isTaken():
        isTaken = User.objects.filter(**{key: value}).count()
        if isTaken:
            return True
        else:
            return False

    if len(value) > 0:

        #Username
        if key == 'username':

            if len(value) <= 6:
                return [False, 'Your username is too short(at least 7 char.)']
            else:
                if re.match('^[A-Za-z0-9_-]*$', value):
                    if isTaken():
                        return[False, 'This username is taken']
                    else:
                        return [True]
                else:
                    return [False, 'Username can containe only letters, numbers, underscores, and hypehens']

        # Email
        if key == 'email':

            if re.search('^.+@[^\.].*\.[a-z]{2,}$', value):
                    if isTaken():
                        return[False, 'This email is taken']
                    else:
                        return [True]
            else:
                return [False, 'Invalid Email']

        # Password
        if key == 'password':

            if len(value) <= 6:
                return [False, 'Your password is too short(7-15)']
            else:
                return [True]

        #Other
        return [True]

    else:

        # Empty Field
        return [False, 'You can\'t submit an empty field']