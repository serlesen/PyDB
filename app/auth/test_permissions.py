import unittest

from app.auth.permissions import Permissions

class PermissionsTest(unittest.TestCase):

    def test_validate_lower_permission(self):
        self.assertTrue(Permissions.validate(Permissions.READ, Permissions.WRITE))

    def test_validate_equals_permission(self):
        self.assertTrue(Permissions.validate(Permissions.READ, Permissions.READ))
        self.assertTrue(Permissions.validate(Permissions.WRITE, Permissions.WRITE))

    def test_not_validated_higher_permission(self):
        self.assertFalse(Permissions.validate(Permissions.WRITE, Permissions.READ))

    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(PermissionsTest)
