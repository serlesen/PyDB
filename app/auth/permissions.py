class Permissions(object):
    READ = 'r'
    WRITE = 'w'

    def validate(desired_permission, user_permision):
        if user_permision == Permissions.WRITE:
            return True
        if desired_permission == user_permision:
            return True
        return False
