class Roles(object):
    """ User type when authenticating.  """

    ADMIN = 'admin'
    REPLICATOR = 'replicator'
    EDITOR = 'editor'
    USER = 'user'

    def validate(requested_role, user_role):
        if requested_role == Roles.REPLICATOR:
            return user_role == Roles.REPLICATOR
        if user_role == Roles.ADMIN:
            return True
        if user_role == Roles.EDITOR and requested_role != Roles.ADMIN:
            return True
        return user_role == requested_role
