import unittest

from pyramid import testing
from pyramid import httpexceptions
from pyramid.decorator import reify

from webob.multidict import MultiDict

from mcmanager import setup_auth, setup_tweens, setup_routes
from .schema import *


# Helper functions
def matchrequest(params=None, **kwargs):
    return testing.DummyRequest(matchdict=kwargs, params=params)

# Globals
URL = 'https://raw.github.com/MCManager/MCManager-Server/master/setup.py'
#URL = 'https://github.com/MCManager/MCManager-Server/archive/master.zip'


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
def create_user(group, username='testuser', email='test@example.com'):
    return User(username=username, password=b'0',
                email=email, group=group).save()


def create_mod(owner, name='TestMod', outdated=False,
               author='SomeAuthor', url='http://someurl.com/'):
    return Mod(
        name=name,
        outdated=outdated,
        rid=name.replace(' ', '_'),
        author=author,
        url=url,
        owner=owner
    )


def mock_mod_data(name='SomeMod'):
    data = {
        'author': 'SAuthor',
        'url': 'http://somevalidurl.com/',
        'target': 'both',
        'install': 'mods',
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
            'install': ['This field is required.'],
            'name': ['This field is required.'],
            'url': ['Invalid URL.']
        })

    def test_add_mod_view(self):
        """ Ensure the add mod page is functional. """
        from urllib.parse import urlparse
        # Create request
        data = mock_mod_data()
        request = testing.DummyRequest(params=MultiDict(data))
        # Get redirect url
        url = self.makeOne(request).addmod().location
        # Get new Mod object
        mod = Mod.objects.get(id=urlparse(url)[2].split('/')[-1])
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
        def flagcheck(ajax):
            old = mod.outdated
            viewclass = self.makeOne(matchrequest(id=mod.id))
            if ajax:
                viewclass.flagmod_ajax()
            else:
                viewclass.flagmod()
            mod.reload()
            self.assertNotEqual(mod.outdated, old)
        # Run it
        flagcheck(False)
        flagcheck(True)

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
