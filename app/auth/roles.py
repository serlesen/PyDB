class Roles(object):
    ADMIN = 'admin'
    EDITOR = 'editor'
    USER = 'user'

    def validate(requested_role, user_role):
        if user_role == Roles.ADMIN:
            return True
        if user_role == Roles.EDITOR and requested_role != Roles.ADMIN:
            return True
        return user_role == requested_role
