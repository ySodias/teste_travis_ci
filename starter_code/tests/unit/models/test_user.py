from section_7.starter_code.models.user import UserModel
from section_7.starter_code.tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test', 'abcd')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'abcd')
