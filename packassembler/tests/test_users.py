import pytest

from base import BaseTest, match_request
from packassembler.schema import User
from factories import UserFactory


@pytest.fixture
def user(request):
    user = UserFactory()

    def fin():
        user.delete()

    request.addfinalizer(fin)
    return user


class TestUserViews(BaseTest):
    def _get_test_class(self):
        from packassembler.views.user import UserViews
        return UserViews

    def user_request(self, user_id):
        return self.make_one(match_request(id=user_id))

    def test_delete_user(self, user):
        self.authenticate(user)
        self.user_request(user.id).deleteuser()
        assert len(User.objects) == 0

    def test_profile(self, user):
        response = self.user_request(user.id).profile()
        assert response['title'] == user.username
        assert response['owner'] == user
