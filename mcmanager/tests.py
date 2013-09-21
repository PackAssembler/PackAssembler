import unittest

from pyramid import testing
from pyramid import httpexceptions

from webob.multidict import MultiDict

from mcmanager import setup_auth, setup_tweens, setup_routes
from .schema import *


# Helper functions
def matchrequest(params=None, **kwargs):
    return testing.DummyRequest(matchdict=kwargs, params=params)


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
def create_user(group):
    return User(username='testuser', password=b'0',
                email='test@example.com', group=group).save()


def create_mod(owner, name='TestMod',
               author='SomeAuthor', url='http://someurl.com/'):
    return Mod(
        name=name,
        rid=name.replace(' ', '_'),
        author=author,
        url=url,
        owner=owner
    )


class DBTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        setup_auth(self.config)
        setup_tweens(self.config)
        setup_routes(self.config)
        self.config.testing_securitypolicy(userid=self.contributor.username)

    def tearDown(self):
        testing.tearDown()

    @classmethod
    def setUpClass(self):
        self.contributor = create_user('contributor')

    def makeOne(self, request):
        """ Returns an object. Should be overwritten. """
        return object()

    @property
    def dummy(self):
        """ Returns a Views instance with a dummy request. """
        return self.makeOne(testing.DummyRequest())


class ModViewTests(DBTests):

    def tearDown(self):
        super().tearDown()
        Mod.drop_collection()

    def makeOne(self, request):
        """ Create a Views instance using the request. """
        from .views.mods import ModViews

        return ModViews(request)

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
        data = {
            'author': 'SAuthor',
            'url': 'http://somevalidurl.com/',
            'target': 'both',
            'install': 'mods',
            'name': 'SomeMod',
            'submit': ''
        }
        request = testing.DummyRequest(params=MultiDict(data))
        # Get redirect url
        url = self.makeOne(request).addmod().location
        # Get new Mod object
        mod = Mod.objects.get(id=urlparse(url)[2].split('/')[-1])
        # Check if information is correct
        self.assertEqual(mod.name, data['name'])
        self.assertEqual(mod.author, data['author'])
        self.assertEqual(mod.url, data['url'])

    def test_delete_mod_view(self):
        """ Ensure the delete mod function actually deletes a mod. """
        # Create a dummy mod.
        mod = create_mod(self.contributor).save()
        # Run deletemod()
        self.makeOne(matchrequest(id=mod.id)).deletemod()
        # Make sure the mod no longer exists
        if Mod.objects(id=mod.id).first():
            fail('Mod still exists.')


class VersionViewTests(DBTests):

    def tearDown(self):
        super().tearDown()
        Mod.drop_collection()
        ModVersion.drop_collection()

    def makeOne(self, request):
        """ Create a Views instance using the request. """
        from .views.modversions import VersionViews

        return VersionViews(request)

    def test_add_mod_version_view_with_mod_file(self):
        """ Ensure add version works with a file upload. """
        from tempfile import TemporaryFile
        # Create a mock file upload using tempfile

        class FileUpload(object):
            pass
        upload = FileUpload()
        upload.file = TemporaryFile()
        upload.file.write(b'Fancy File')
        upload.file.seek(0)
        # Create a dummy mod
        mod = create_mod(self.contributor).save()
        # Create request
        data = {
            'version': '1.0.0',
            'mc_min': MCVERSIONS[0],
            'mc_max': MCVERSIONS[0],
            'forge_min': '0.00.0.000',
            'forge_max': '0.00.0.000',
            'devel': True,
            'mod_file': upload,
            'mod_file_url': '',
            'submit': ''
        }
        request = matchrequest(params=MultiDict(data), id=mod.id)
        # Run
        self.makeOne(request).addversion()
        # Reload the mod
        mod.reload()
        # Check if the mod has a new version
        self.assertTrue(mod.versions)
        # Assign an easy-to-use variable to the version
        v = mod.versions[0]
        # Check if content of file is the same
        upload.file.seek(0)
        self.assertEqual(v.mod_file.read(), upload.file.read())
        # Check if the attributes of the version are the same
        self.assertEqual(v.version, data['version'])
        self.assertEqual(v.mc_max, data['mc_max'])
        # Close the test file
        upload.file.close()
