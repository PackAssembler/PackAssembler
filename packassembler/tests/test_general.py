from packassembler.views.general import GeneralViews
from base import DummyRequest, BaseTest


class TestGeneralView(BaseTest):
    def test_home(self):
        response = GeneralViews(DummyRequest()).home()
        assert response['title'] == 'Home'
