import unittest

from app.auth.roles import Roles


class RolesTest(unittest.TestCase):

    def test_validate_lower_role(self):
        self.assertTrue(Roles.validate(Roles.EDITOR, Roles.ADMIN))
        self.assertTrue(Roles.validate(Roles.USER, Roles.ADMIN))

    def test_validate_equals_role(self):
        self.assertTrue(Roles.validate(Roles.ADMIN, Roles.ADMIN))
        self.assertTrue(Roles.validate(Roles.EDITOR, Roles.EDITOR))

    def test_not_validated_higher_role(self):
        self.assertFalse(Roles.validate(Roles.ADMIN, Roles.EDITOR))
        self.assertFalse(Roles.validate(Roles.ADMIN, Roles.USER))
        self.assertFalse(Roles.validate(Roles.EDITOR, Roles.USER))

    def test_not_validated_user_role(self):
        self.assertTrue(Roles.validate(Roles.USER, Roles.USER))

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(RolesTest)
