import pytest

from base import BaseTest, match_request, DummyRequest
from packassembler.schema import Pack
from factories import PackFactory
from webob.multidict import MultiDict


@pytest.fixture
def pack(request):
    pack = PackFactory()

    def fin():
        pack.owner.delete()
        pack.delete()

    request.addfinalizer(fin)
    return pack


def pack_to_data(pack):
    data = pack._data
    data['submit'] = ''
    return data


class TestPackViews(BaseTest):
    def _get_test_class(self):
        from packassembler.views.packs import PackViews
        return PackViews

    def pack_request(self, pack_id, params=None, **kwargs):
        return self.make_one(match_request(params=params, id=pack_id, **kwargs))

    def test_pack_list_with_no_packs(self):
        """ Ensure the packlist returns no packs. """
        response = self.make_one(DummyRequest()).packlist()
        assert len(response['packs']) == 0

    def test_pack_list_with_packs(self, pack):
        """ Ensure the packlist returns packs when they exist. """
        # Create another dummy pack
        pack2 = PackFactory(owner=pack.owner)
        # Get result
        response = self.make_one(DummyRequest()).packlist()
        # Check the packs
        assert len(response['packs']) == 2
        assert response['packs'][0] == pack
        assert response['packs'][1] == pack2
        # Delete the second dummy pack
        pack2.delete()

    def test_add_pack_view(self, pack):
        """ Ensure the add pack page is functional. """
        # Generate request
        request = DummyRequest(params=MultiDict(pack_to_data(pack)))
        # Run
        self.authenticate(pack.owner)
        self.make_one(request).addpack()
        # Get new Pack object
        new_pack = Pack.objects.get()
        # Check if information is correct
        assert new_pack.name == pack.name

    def test_edit_pack_view(self, pack):
        """ Ensure the edit pack page is functional. """
        # Generate request
        data = pack_to_data(pack)
        data['name'] = 'SomeNewName'
        request = self.pack_request(pack.id, params=MultiDict(data))
        # Run
        self.authenticate(pack.owner)
        self.make_one(request).editpack()
        # Get the new Pack object
        new_pack = Pack.objects.get()
        # Check if information is correct
        assert new_pack.name != pack.name
        assert new_pack.name == 'SomeNewName'
