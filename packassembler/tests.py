import unittest

from pyramid import testing
from pyramid import httpexceptions
from pyramid.decorator import reify

from webob.multidict import MultiDict

from packassembler import setup_auth, setup_tweens, setup_routes
from .schema import *


# Helper functions
def matchrequest(params=None, **kwargs):
    return testing.DummyRequest(matchdict=kwargs, params=params)

# Globals
URL = 'http://mml.stephenmac.com/static/archives/config.zip'
IMG = 'http://placekitten.com/g/2000/600'


class GeneralViewTests(unittest.TestCase):

    """ Tests for more static views, don't contact db. """

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def makeOne(self, request):
        """ Creates a Views instance using the request. """
        from .views.general import GeneralViews

        return GeneralViews(request)

    @property
    def dummy(self):
        """ Returns a Views instance with a dummy request. """
        return self.makeOne(testing.DummyRequest())

    def test_home_view(self):
        """ Tests the home view, should have the title home. """
        result = self.dummy.home()
        self.assertEqual(result['title'], 'Home')

    def test_error_view(self):
        """ Error view should return correct message for an error type. """
        request = matchrequest(type='already_cloned')
        result = self.makeOne(request).error()
        self.assertIn('already cloned this pack', result['message'])


# DB helper functions
create_rid = lambda name: name.replace(' ', '_')


def create_user(group, username='testuser', email='test@example.com'):
    return User(username=username, password=b'0',
                email=email, group=group).save()


def create_mod(owner, name='TestMod', outdated=False,
               author='SomeAuthor', url='http://someurl.com/'):
    return Mod(
        name=name,
        outdated=outdated,
        rid=create_rid(name),
        author=author,
        url=url,
        owner=owner
    )


def create_pack(owner, name='TestPack', devel=False, **kwargs):
    return Pack(
        name=name, rid=create_rid(name), devel=devel,
        owner=owner, **kwargs)


def mock_mod_data(name='SomeMod'):
    data = {
        'author': 'SAuthor',
        'url': 'http://somevalidurl.com/',
        'target': 'both',
        'name': name,
        'submit': ''
    }

    return data


def mock_version_data(mc_min=MCVERSIONS[0], mc_max=MCVERSIONS[0], forge_min='',
                      forge_max='', mod_file=None, mod_file_url=''):
    """ Create mock data for a mod version. """
    data = {
        'version': '1.0.0',
        'mc_min': mc_min,
        'mc_max': mc_max,
        'forge_min': forge_min,
        'forge_max': forge_max,
        'devel': True,
        'mod_file': mod_file,
        'mod_file_url': mod_file_url,
        'submit': ''
    }

    return data


def mock_pack_data(name='SomePack', devel=False):
    """ Creates mock data to create a pack. """
    data = {
        'name': name,
        'submit': ''
    }
    if devel:
        data['devel'] = True

    return data


class DBTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        setup_auth(self.config)
        setup_tweens(self.config)
        setup_routes(self.config)
        self.config.testing_securitypolicy(userid=self.contributor.username)

    def tearDown(self):
        testing.tearDown()

    @reify
    def contributor(self):
        return create_user('contributor')

    def makeOne(self, request):
        """ Returns an object. Should be overwritten. """
        return object()

    @property
    def dummy(self):
        """ Returns a Views instance with a dummy request. """
        return self.makeOne(testing.DummyRequest())


class ModViewTests(DBTests):

    @classmethod
    def setUpClass(self):
        self.orphan = create_user('orphan', username='Orphan', email='orphan@example.com')

    def tearDown(self):
        super().tearDown()
        Mod.drop_collection()

    def makeOne(self, request):
        """ Create a Views instance using the request. """
        from .views.mods import ModViews

        return ModViews(request)

    def check_mod(self, mod, data):
        self.assertEqual(mod.name, data['name'])
        self.assertEqual(mod.author, data['author'])
        self.assertEqual(mod.url, data['url'])

    def test_mod_list_view_with_no_mods(self):
        """ Ensure the modlist returns no mods. """
        result = self.dummy.modlist()
        self.assertFalse(result['mods'])

    def test_mod_list_view_with_mods(self):
        """ Ensure the modlist returns mods when they exist. """
        # Create dummy mods
        mod = create_mod(self.contributor, name='aMod').save()
        mod2 = create_mod(self.contributor, name='bMod').save()
        # Get result
        result = self.dummy.modlist()
        # Make sure the names are the same as the ones in the result list
        self.assertEqual(result['mods'][0].name, mod.name)
        self.assertEqual(result['mods'][1].name, mod2.name)

    def test_mod_list_view_with_mods_and_search(self):
        """
        Ensure the modlist returns only matching mods when
        a query is given.
        """
        # Create dummy mods
        create_mod(self.contributor, name='aMod').save()
        mod = create_mod(self.contributor, name='bMod').save()
        # Get result
        result = self.makeOne(
            testing.DummyRequest(params={'q': 'b'})).modlist()
        # Make sure there is only one mod
        self.assertTrue(len(result['mods']) == 1)
        self.assertEqual(result['mods'][0].name, mod.name)

    def test_mod_view_object(self):
        """ Ensure the mod view returns the correct mod object. """
        # Create dummy mod
        mod = create_mod(self.contributor).save()
        # Get result
        result = self.makeOne(matchrequest(id=mod.id)).viewmod()
        # Make sure there is information which matches with the mod in the page
        self.assertEqual(result['mod'].name, mod.name)
        self.assertEqual(result['mod'].author, mod.author)
        self.assertEqual(result['mod'].url, mod.url)

    def test_add_mod_view_with_bad_input(self):
        """ Ensure the add mod page is validated by inputting bad info. """
        # Create request
        request = testing.DummyRequest(params=MultiDict({
            'author': 'SAuthor',
            'url': 'somehomepage',
            'target': 'both',
            'submit': ''
        }))
        # Get result and make sure it's not HTTPFound
        try:
            result = self.makeOne(request).addmod()
        except httpexceptions.HTTPFound:
            self.fail('Bad input was accepted.')

        # Check if the correct errors are returned
        self.assertDictEqual(result['f'].errors, {
            'name': ['This field is required.'],
            'url': ['Invalid URL.']
        })

    def test_add_mod_view(self):
        """ Ensure the add mod page is functional. """
        # Create request
        data = mock_mod_data()
        request = testing.DummyRequest(params=MultiDict(data))
        # Run
        self.makeOne(request).addmod()
        # Get new Mod object
        mod = Mod.objects().first()
        # Check if information is correct
        self.check_mod(mod, data)

    def test_edit_mod_view(self):
        """ Ensure the edit mod view is functional. """
        # Create dummy mod.
        mod = create_mod(self.contributor).save()
        # Create request
        data = mock_mod_data(name='SomeOtherMod')
        request = matchrequest(id=mod.id, params=MultiDict(data))
        # Run it
        self.makeOne(request).editmod()
        # Reload the mod object
        mod.reload()
        # Check if the information is correct
        self.check_mod(mod, data)

    def test_delete_mod_view(self):
        """ Ensure the delete mod function actually deletes a mod. """
        # Create a dummy mod.
        mod = create_mod(self.contributor).save()
        # Run deletemod()
        self.makeOne(matchrequest(id=mod.id)).deletemod()
        # Make sure the mod no longer exists
        self.assertIsNone(Mod.objects(id=mod.id).first())

    def test_flag_mod_view(self):
        """ Ensure the flag mod view changes the outdated boolean. """
        # Create a dummy mod.
        mod = create_mod(self.contributor, outdated=False).save()

        # Create checking function
        def runflag(ajax):
            viewclass = self.makeOne(matchrequest(id=mod.id))
            if ajax:
                viewclass.flagmod_ajax()
            else:
                viewclass.flagmod()
            mod.reload()
        # Run it (no ajax)
        runflag(False)
        self.assertEqual(mod.outdated, True)
        runflag(False)
        self.assertEqual(mod.outdated, False)
        # Run it (with ajax)
        runflag(True)
        self.assertEqual(mod.outdated, True)
        runflag(False)
        self.assertEqual(mod.outdated, False)

    def test_disown_mod_view(self):
        """ Ensure the disown view works. """
        # Create a dummy mod.
        mod = create_mod(self.contributor).save()

        # Run disown()
        self.makeOne(matchrequest(id=mod.id)).disown()
        # Check if it's no longer owned by contributor
        mod.reload()
        self.assertNotEqual(mod.owner, self.contributor)

    def test_adopt_mod_view(self):
        """ Ensure the adopt view works. """
        # Create a dummy mod.
        mod = create_mod(self.orphan).save()

        # Run adopt()
        self.makeOne(matchrequest(id=mod.id)).adopt()
        # Check if contributor is the new owner
        mod.reload()
        self.assertEqual(mod.owner.username, self.contributor.username)

    def test_edit_banner_view_with_an_image(self):
        """ Ensure edit banner actually saves an image in banner.image. """
        # Create a dummy mod.
        mod = create_mod(self.contributor).save()

        # Create request
        request = matchrequest(
            params=MultiDict({'image': IMG, 'submit': ''}), id=mod.id)
        # Run
        self.makeOne(request).editbanner()
        # Check if the image has changed
        mod.reload()
        self.assertEqual(mod.banner.image, IMG)

    def test_edit_banner_with_with_no_image(self):
        """ Ensure the banner object is gone when there is no image. """
        # Create a dummy mod.
        mod = create_mod(self.contributor).save()
        # Add a banner
        mod.banner = Banner()
        mod.banner.image = IMG
        mod.save()

        # Create request
        request = matchrequest(
            params=MultiDict({'text_color': '#000000', 'submit': ''}),
            id=mod.id)
        # Run
        self.makeOne(request).editbanner()
        # Check if no banner exists
        mod.reload()
        self.assertIsNone(mod.banner)


class VersionViewTests(DBTests):

    def tearDown(self):
        super().tearDown()
        Mod.drop_collection()
        ModVersion.drop_collection()

    def makeOne(self, request):
        """ Create a Views instance using the request. """
        from .views.modversions import VersionViews

        return VersionViews(request)

    def create_mock_file(self, data):
        """ Create a mock file upload using tempfile. """
        from tempfile import TemporaryFile

        class FileUpload(object):
            pass
        upload = FileUpload()
        upload.file = TemporaryFile()
        upload.file.write(data)
        upload.file.seek(0)

        return upload

    @reify
    def mock_file(self):
        """ Default mock file. """
        from urllib.request import urlopen

        return self.create_mock_file(urlopen(URL).read())

    def check_general(self, v, data):
        """ Checks general information about the version object. """
        self.assertEqual(v.version, data['version'])
        self.assertEqual(v.mc_min, data['mc_min'])
        self.assertEqual(v.mc_max, data['mc_max'])

    def check_mod_file(self, v, data):
        self.assertIsNotNone(v.mod_file)
        # Check if content of file is the same
        data['mod_file'].file.seek(0)
        self.assertEqual(
            self.download_version(v).body, data['mod_file'].file.read())
        # Make sure mod_file_url and mod_file_url_md5 are not filled out
        self.assertIsNone(v.mod_file_url)
        self.assertIsNone(v.mod_file_url_md5)
        # Check if the attributes of the version are the same
        self.check_general(v, data)
        # Close the test file
        data['mod_file'].file.close()

    def check_mod_file_url(self, v, data):
        from urllib.request import urlopen
        # Check if the url is correct
        self.assertEqual(v.mod_file_url, data['mod_file_url'])
        # Check for an md5
        self.assertEqual(len(v.mod_file_url_md5), 32)
        # Check if the actual file is the same
        self.assertEqual(
            urlopen(URL).read(),
            urlopen(self.download_version(v).location).read())
        # Make sure mod_file is not filled out
        self.assertFalse(v.mod_file)
        # Check if the attributes of the version are the same
        self.check_general(v, data)

    def download_version(self, version):
        """ Downloads mod version using downloadversion. """
        request = matchrequest(id=version.id)
        return self.makeOne(request).downloadversion()

    def test_add_mod_version_view_with_mod_file(self):
        """ Ensure add version works with a file upload. """
        # Create a dummy mod
        mod = create_mod(self.contributor).save()
        # Create request
        data = mock_version_data(mod_file=self.mock_file)
        request = matchrequest(params=MultiDict(data), id=mod.id)
        # Run
        self.makeOne(request).addversion()
        # Reload the mod
        mod.reload()
        # Assign an easy-to-use variable to the version
        v = mod.versions[0]
        # Run tests
        self.check_mod_file(v, data)

    def test_add_mod_version_with_valid_url(self):
        """ Ensure add version works with a valid mod file url. """
        # Create a dummy mod.
        mod = create_mod(self.contributor).save()
        # Create request
        data = mock_version_data(mod_file_url=URL)
        request = matchrequest(params=MultiDict(data), id=mod.id)
        # Run
        self.makeOne(request).addversion()
        # Reload the mod
        mod.reload()
        # Check if the mod has a new version
        self.assertTrue(mod.versions)
        # Assign an easy-to-user variable to the version
        v = mod.versions[0]
        # Run tests
        self.check_mod_file_url(v, data)

    def test_add_mod_version_with_url_and_mod_file(self):
        """
        Ensure add version only uses the mod file when both mod_file and
        mod_file_url are provided.
        """
        # Create a dummy mod
        mod = create_mod(self.contributor).save()
        # Create request
        data = mock_version_data(mod_file=self.mock_file, mod_file_url=URL)
        request = matchrequest(params=MultiDict(data), id=mod.id)
        # Run
        self.makeOne(request).addversion()
        # Reload the mod
        mod.reload()
        # Assign an easy-to-use variable to the version
        v = mod.versions[0]
        # Run tests
        self.check_mod_file(v, data)

    def test_edit_mod_version_with_new_mod_file(self):
        """
        Ensure edit version actually changes the mod file if a new one
        is added.
        """
        # Create a dummy mod
        mod = create_mod(self.contributor).save()
        # Create a modversion
        self.makeOne(matchrequest(
            params=MultiDict(mock_version_data(mod_file=self.mock_file)),
            id=mod.id)).addversion()
        # Reload the mod
        mod.reload()
        # Get the new modversion
        v = mod.versions[0]
        # Create request
        data = mock_version_data(mod_file=self.create_mock_file(b'Testdata'))
        request = matchrequest(params=MultiDict(data), id=v.id)
        # Run
        self.makeOne(request).editversion()
        # Reload the version
        v.reload()
        # Run tests
        self.check_mod_file(v, data)

    def test_edit_mod_version_switching_to_mod_file_url(self):
        """
        Ensure edit version actually deletes the mod_file if we
        switch to mod_file_url.
        """
        # Create a dummy mod
        mod = create_mod(self.contributor).save()
        # Create a modversion
        self.makeOne(matchrequest(
            params=MultiDict(mock_version_data(mod_file=self.mock_file)),
            id=mod.id)).addversion()
        # Reload the mod
        mod.reload()
        # Get the new modversion
        v = mod.versions[0]
        # Create request
        data = mock_version_data(mod_file_url=URL)
        request = matchrequest(params=MultiDict(data), id=v.id)
        # Run
        self.makeOne(request).editversion()
        # Reload the version
        v.reload()
        # Run tests
        self.check_mod_file_url(v, data)

    def test_edit_mod_version_switching_to_mod_file(self):
        """
        Ensure edit version actually switches to mod_file if we
        want to change from mod_file_url.
        """
        # Create a dummy mod
        mod = create_mod(self.contributor).save()
        # Create a modversion
        self.makeOne(matchrequest(
            params=MultiDict(mock_version_data(mod_file_url=URL)),
            id=mod.id)).addversion()
        # Reload the mod
        mod.reload()
        # Get the new modversion
        v = mod.versions[0]
        # Create request
        data = mock_version_data(mod_file=self.mock_file, mod_file_url=URL)
        request = matchrequest(params=MultiDict(data), id=v.id)
        # Run
        self.makeOne(request).editversion()
        # Reload the version
        v.reload()
        # Run tests
        self.check_mod_file(v, data)

    def test_edit_mod_version_with_no_file_input(self):
        """
        Ensure edit version preserves previous files on edit.
        """
        # Create a dummy mod
        mod = create_mod(self.contributor).save()
        # Create a modversion
        self.makeOne(matchrequest(
            params=MultiDict(mock_version_data(mod_file=self.mock_file)),
            id=mod.id)).addversion()
        # Reload the mod
        mod.reload()
        # Get the new modversion
        v = mod.versions[0]
        # Create request
        data = mock_version_data()
        request = matchrequest(params=MultiDict(data), id=v.id)
        data['mod_file'] = self.mock_file
        # Run
        self.makeOne(request).editversion()
        # Reload the version
        v.reload()
        # Run tests
        self.check_mod_file(v, data)

    def test_delete_version_with_mod_file(self):
        """ Ensure delete version actually deletes the mod_file. """
        from gridfs import GridFS
        from mongoengine.connection import get_db
        # Create a dummy mod
        mod = create_mod(self.contributor).save()
        # Create a modversion
        self.makeOne(matchrequest(
            params=MultiDict(mock_version_data(mod_file=self.mock_file)),
            id=mod.id)).addversion()
        # Reload the mod
        mod.reload()
        # Get the new modversion
        v = mod.versions[0]
        # Create a variable for the mod_file
        mf_id = v.mod_file.grid_id
        # Create request to delete the new modversion
        request = matchrequest(id=v.id)
        # Run
        self.makeOne(request).deleteversion()
        # Reload the mod again
        mod.reload()
        # Check if the version's gone
        self.assertFalse(mod.versions)
        # Check if the mod file has been deleted
        self.assertFalse(GridFS(get_db(), collection='modfs').exists(mf_id))

    def test_delete_version_with_mod_file_url(self):
        """ Ensure delete version works with no mod_file. """
        # Create a dummy mod
        mod = create_mod(self.contributor).save()
        # Create a modversion
        self.makeOne(matchrequest(
            params=MultiDict(mock_version_data(mod_file_url=URL)),
            id=mod.id)).addversion()
        # Reload the mod
        mod.reload()
        # Get the new modversion
        v = mod.versions[0]
        # Create request to delete the new modversion
        request = matchrequest(id=v.id)
        # Run
        self.makeOne(request).deleteversion()
        # Reload the mod again
        mod.reload()
        # Check if the version's gone
        self.assertFalse(mod.versions)


class PackViewTests(DBTests):

    def tearDown(self):
        super().tearDown()
        Pack.drop_collection()

    def makeOne(self, request):
        """ Create a Views instance using the request. """
        from .views.packs import PackViews

        return PackViews(request)

    def check_pack(self, pack, data):
        self.assertEqual(pack.name, data['name'])
        if 'devel' in data:
            self.assertEqual(pack.devel, data['devel'])

    def test_pack_list_view_with_no_packs(self):
        """ Ensure the packlist returns no packs. """
        result = self.dummy.packlist()
        self.assertFalse(result['packs'])

    def test_pack_list_view_with_packs(self):
        """ Ensure the packlist returns packs when they exist. """
        # Create dummy packs
        pack = create_pack(self.contributor, name='aPack').save()
        pack2 = create_pack(self.contributor, name='bPack').save()
        # Get result
        result = self.dummy.packlist()
        # Check the packs
        self.check_pack(result['packs'][0], pack)
        self.check_pack(result['packs'][1], pack2)

    def test_pack_list_view_with_packs_and_search(self):
        """
        Ensure the packlist only returns matching packs when a query
        is given.
        """
        # Create dummy packs
        create_pack(self.contributor, name='aPack').save()
        pack2 = create_pack(self.contributor, name='bPack').save()
        # Get result
        result = self.makeOne(
            testing.DummyRequest(params={'q': 'b'})).packlist()
        # Check the listing
        self.assertTrue(len(result['packs']) == 1)
        self.check_pack(result['packs'][0], pack2)

    def test_add_mod_view(self):
        """ Ensure the add pack page is functional. """
        # Create request
        data = mock_pack_data()
        request = testing.DummyRequest(params=MultiDict(data))
        # Run
        self.makeOne(request).addpack()
        # Get new Pack object
        pack = Pack.objects().first()
        # Check if information is correct
        self.check_pack(pack, data)

    def test_edit_pack_view(self):
        """ Ensure the edit pack page is functional. """
        # Create dummy pack
        pack = create_pack(self.contributor).save()
        # Create request
        data = mock_pack_data(name='NewName', devel=True)
        request = matchrequest(id=pack.id, params=MultiDict(data))
        # Run
        self.makeOne(request).editpack()
        # Check if information is correct
        pack.reload()
        self.check_pack(pack, data)

    def test_clone_pack_view(self):
        """ Ensure the clone pack view is functional. """
        # Create dummy pack
        pack = create_pack(self.contributor).save()
        # Create request
        request = matchrequest(id=pack.id)
        # Run
        runner = self.makeOne(request)
        runner.clonepack()
        # Check if the pack has been cloned
        cpack = Pack.objects.get(name__contains=self.contributor.username)
        # Check if it's in fact cloned
        self.assertEqual(cpack.devel, pack.devel)
        self.assertIn(pack.name, cpack.name)
        # Try again, should return an error page
        response = runner.clonepack()
        self.assertIn('error', response.location)

    def test_delete_pack_view(self):
        """ Ensure the delete pack view is functional. """
        # Create dummy pack
        pack = create_pack(self.contributor).save()
        # Create request
        request = matchrequest(id=pack.id)
        # Run
        self.makeOne(request).deletepack()
        # Make sure it's gone
        self.assertIsNone(Pack.objects(id=pack.id).first())

    @unittest.skip
    def test_delete_pack_view_where_a_server_depends_on_the_pack(self):
        """ Ensure a pack is not deleted if a server requires the pack. """
        # Create dummy pack
        #pack = create_pack(self.contributor).save()

    def test_view_pack_object(self):
        """ Ensure the view page returns the correct object. """
        # Create a dummy pack
        pack = create_pack(self.contributor).save()
        # Create request
        request = matchrequest(id=pack.id)
        # Run
        response = self.makeOne(request).viewpack()
        # Check it
        self.check_pack(response['pack'], pack)

    def test_addpackmod_view(self):
        """ Ensure the add pack mod view works. """
        # Create dummy mods
        mod = create_mod(self.contributor, name='aMod').save()
        mod2 = create_mod(self.contributor, name='bMod').save()
        # Create dummy pack
        pack = create_pack(self.contributor).save()
        # Create request
        data = MultiDict()
        data.add('mods', mod.id)
        data.add('mods', mod2.id)
        request = matchrequest(id=pack.id, params=data)
        # Run
        self.makeOne(request).addpackmod()
        # Check it
        pack.reload()
        self.assertIn(mod, pack['mods'])
        self.assertIn(mod2, pack['mods'])

    def test_removepackmod_view(self):
        """ Ensure the remove pack mod view works. """
        # Create dummy mod
        mod = create_mod(self.contributor).save()
        # Create dummy pack
        pack = create_pack(self.contributor, mods=[mod]).save()
        # Create request
        request = matchrequest(packid=pack.id, modid=mod.id)
        # Run
        self.makeOne(request).removepackmod()
        # Check it
        pack.reload()
        self.assertFalse(pack.mods)
