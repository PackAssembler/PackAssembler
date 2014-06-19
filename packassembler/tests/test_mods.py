import pytest

from base import BaseTest, match_request, DummyRequest, document_to_data
from packassembler.schema import Mod
from factories import ModFactory
from webob.multidict import MultiDict


@pytest.fixture
def mod(request):
    mod = ModFactory()

    def fin():
        mod.owner.delete()
        mod.delete()

    request.addfinalizer(fin)
    return mod


@pytest.fixture
def mod_unsaved(request):
    return ModFactory.build()


def check_mod(moda, modb):
    assert moda.name == modb.name
    assert moda.author == modb.author
    assert moda.url == modb.url


class TestModViews(BaseTest):
    def _get_test_class(self):
        from packassembler.views.mods import ModViews
        return ModViews

    # List tests - add search tests
    def test_mod_list_with_no_mods(self):
        """ Ensure the modlist returns no mods. """
        response = self.make_one(DummyRequest()).modlist()
        assert len(response['mods']) == 0

    def test_mod_list_with_mods(self, mod):
        """ Ensure the modlist returns mods when they exist. """
        # Create another dummy pack
        mod2 = ModFactory(owner=mod.owner)
        # Get result
        response = self.make_one(DummyRequest()).modlist()
        # Check the packs
        assert len(response['mods']) == 2
        assert response['mods'][0] == mod
        assert response['mods'][1] == mod2
        # Delete the second dummy pack
        mod2.delete()

    # CRUD tests - add bad input tests
    def test_view_mod_view(self, mod):
        """ Ensure the view mod page is functional. """
        # Make sure the mod returned is the same as the original
        response = self.make_one(match_request(id=mod.id)).viewmod()
        assert response['mod'] == mod

    def test_add_mod_view(self, mod_unsaved):
        """ Ensure the add mod page is functional. """
        # Generate request
        request = DummyRequest(params=MultiDict(document_to_data(mod_unsaved)))
        # Run
        self.authenticate(mod_unsaved.owner)
        self.make_one(request).addmod()
        # Get new Mod object
        new_mod = Mod.objects.get()
        # Check if information is correct
        assert new_mod.name == mod_unsaved.name
        # Remove the mod in the interest of keeping the db clean
        new_mod.delete()

    def test_edit_mod_view(self, mod):
        """ Ensure the edit mod page is functional. """
        # Generate request
        data = document_to_data(mod)
        data['name'] = 'SomeNewName'
        request = match_request(id=mod.id, params=MultiDict(data))
        # Run
        self.authenticate(mod.owner)
        self.make_one(request).editmod()
        # Get the new Mod object
        new_mod = Mod.objects.get()
        # Check if information is correct
        assert new_mod.name != mod.name
        assert new_mod.name == 'SomeNewName'

    def test_delete_mod_view(self, mod):
        """ Ensure the delete mod view is functional. """
        # Create request
        request = match_request(id=mod.id)
        # Run
        self.authenticate(mod.owner)
        self.make_one(request).deletemod()
        # Make sure it's gone
        assert Mod.objects(id=mod.id).first() is None

    # Extra action tests
    def test_flag_mod_view(self, mod):
        """ Ensure the flag mod view changes the outdated boolean. """
        viewclass = self.make_one(match_request(id=mod.id))
        # Create checking function
        def runflag(ajax):
            if ajax:
                viewclass.flagmod_ajax()
            else:
                viewclass.flagmod()
            mod.reload()

        # Run it (no ajax)
        runflag(False)
        assert mod.outdated
        runflag(False)
        assert not mod.outdated
        # Run it (with ajax)
        runflag(True)
        assert mod.outdated
        runflag(False)
        assert not mod.outdated

    def test_disown_mod_view(self, mod):
        """ Ensure the disown view works. """
        # Get original owner for cleanup
        owner = mod.owner
        # Run disown()
        self.make_one(match_request(id=mod.id)).disown()
        # Check if it's no longer owned by contributor
        mod.reload()
        assert mod.owner is None
        # Reset for finish
        mod.owner = owner
        mod.save()

    def test_adopt_mod_view(self, mod):
        """ Ensure the adopt view works. """
        # Get mod's current username and authenticate with it
        target = mod.owner
        self.authenticate(target)
        # Make the mod have no owner
        mod.owner = None
        mod.save()
        # Run adopt()
        self.make_one(match_request(id=mod.id)).adopt()
        # Check if contributor is the new owner
        mod.reload()
        assert mod.owner.id == target.id

    def test_quickmod_view(self, mod):
        """ Ensure the quickmod view works. """
        # Create request
        request = match_request(id=mod.id)
        # Run
        response = self.make_one(request).quickmod()
        # Make sure the response at least has some things right
        assert response['name'] == mod.name
        assert len(response['versions']) == len(mod.versions)
