from unittest.mock import MagicMock

from flask_jwt_extended.exceptions import UserClaimsVerificationError

from libs.jwt_functions import verify_jwt_admin_claim
from NotesApp.tests.base_test import BaseTest


class TestAdminClaims(BaseTest):

    def test_checking_not_admin_raises_error(self):
        jwt_data = MagicMock(spec=dict)
        jwt_data.get = MagicMock(return_value=None)
        with self.assertRaises(UserClaimsVerificationError):
            verify_jwt_admin_claim(
                jwt_header={},
                jwt_data=jwt_data,
                admin=True,
            )
        jwt_data.get.assert_called_once_with("admin")

    def test_checking_admin_not_raises_error(self):
        jwt_data = MagicMock(spec=dict)
        jwt_data.get = MagicMock(return_value="True")
        verify_jwt_admin_claim(
            jwt_header={},
            jwt_data=jwt_data,
            admin=True,
        )
        jwt_data.get.assert_called_once_with("admin")
