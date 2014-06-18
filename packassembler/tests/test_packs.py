import pytest

from base import BaseTest, match_request, DummyRequest, document_to_data
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


class TestPackViews(BaseTest):
    def _get_test_class(self):
        from packassembler.views.packs import PackViews
        return PackViews

    # List tests - add search tests
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

    # CRUD tests - add bad input tests
    def test_view_pack_view(self, pack):
        """ Ensure the view pack page is functional. """
        # Make sure the pack returned is the same as the original
        response = self.make_one(match_request(id=pack.id)).viewpack()
        assert response['pack'] == pack

    def test_add_pack_view(self, pack):
        """ Ensure the add pack page is functional. """
        # Generate request
        request = DummyRequest(params=MultiDict(document_to_data(pack)))
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
        data = document_to_data(pack)
        data['name'] = 'SomeNewName'
        request = match_request(id=pack.id, params=MultiDict(data))
        # Run
        self.authenticate(pack.owner)
        self.make_one(request).editpack()
        # Get the new Pack object
        new_pack = Pack.objects.get()
        # Check if information is correct
        assert new_pack.name != pack.name
        assert new_pack.name == 'SomeNewName'

    def test_delete_pack_view(self, pack):
        """ Ensure the delete pack view is functional. """
        # Create request
        request = match_request(id=pack.id)
        # Run
        self.authenticate(pack.owner)
        self.make_one(request).deletepack()
        # Make sure it's gone
        assert Pack.objects(id=pack.id).first() is None

    # Extra action tests
    def test_clone_pack_view(self, pack):
        """ Ensure the clone pack view is functional. """
        # Generate request
        request = match_request(id=pack.id)
        # Run
        self.authenticate(pack.owner)
        runner = self.make_one(request)
        runner.clonepack()
        # Check whether cloning actually happened
        cpack = Pack.objects.get(name__contains=pack.owner.username)
        assert pack.name in cpack.name
        # Run again, should fail
        runner.clonepack()
        assert 'already' in request.session['error_flash'][0].lower()
