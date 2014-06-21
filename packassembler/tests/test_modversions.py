import pytest
import requests

from base import BaseTest, match_request, document_to_data
from packassembler.schema import ModVersion
from factories import ModVersionFactory, ModFactory
from webob.multidict import MultiDict
from unittest import mock

URL = 'http://bit.ly/1uM5XgB'
slow_skip = pytest.mark.skipif(False, reason="too slow")

@pytest.fixture
def mod(request):
    mod = ModFactory()

    def fin():
        mod.owner.delete()
        mod.delete()

    request.addfinalizer(fin)
    return mod


@pytest.fixture
def mv(request, mod, file_content):
    mv = ModVersionFactory(mod=mod, mod_file=file_content)
    mod.versions.append(mv)
    mod.save()

    def fin():
        if mv.mod_file:
            mv.mod_file.delete()
        mv.delete()

    request.addfinalizer(fin)
    return mv


@pytest.fixture
def file_content(request):
    return requests.get(URL).content


@pytest.fixture
def mock_upload(file_content):
    upload = mock.Mock()
    upload.file = file_content
    return upload


def generate_mv_build(upload_type, upload=None, base=None):
    # Generate seed data
    mv_build = document_to_data(base or ModVersionFactory.build())
    mv_build['upload_type'] = upload_type
    del mv_build['depends']

    if upload_type in ['direct', 'url_upload']:
        mv_build['mod_file_url'] = URL
    else:
        mv_build['mod_file'] = upload

    return mv_build


# Verifiers
def verify_direct(mv):
    assert not mv.mod_file
    assert mv.mod_file_url[0:4] == 'http'
    assert len(mv.mod_file_url_md5) == 32


def verify_upload(mv):
    assert mv.mod_file
    assert mv.mod_file_url is None
    assert mv.mod_file_url_md5 is None


class TestVersionViews(BaseTest):
    def _get_test_class(self):
        from packassembler.views.modversions import VersionViews
        return VersionViews

    def add_test_helper(self, mod, upload_type, upload=None):
        mv_build = generate_mv_build(upload_type, upload)

        request = match_request(id=mod.id, params=MultiDict(mv_build))
        self.authenticate(mod.owner)
        self.make_one(request).addversion()

        # Get our new version
        new_mv = ModVersion.objects.get()

        assert new_mv.version == mv_build['version']
        return new_mv

    def edit_test_helper(self, mv, upload_type):
        """ Ensure the edit version page is functional. """
        # Generate request and data
        data = generate_mv_build(upload_type, base=mv)
        data['version'] = '9.3.0'
        request = match_request(id=mv.id, params=MultiDict(data))
        # Run
        self.authenticate(mv.mod.owner)
        self.make_one(request).editversion()
        # Get the new Mod object
        new_mv = ModVersion.objects.get()
        # Check if information is correct
        assert new_mv.version != mv.version
        assert new_mv.version == data['version']

        return new_mv


    # CRUD tests
    @slow_skip
    def test_add_view_with_direct_link(self, mod):
        """ Ensure the add version page is functional. """
        new_mv = self.add_test_helper(mod, 'direct')
        verify_direct(new_mv)

    @slow_skip
    def test_add_view_with_file_upload(self, mod, mock_upload):
        """ Ensure the add version page works when using a file upload. """
        new_mv = self.add_test_helper(mod, 'upload', mock_upload)
        verify_upload(new_mv)

    @slow_skip
    def test_add_view_with_url_upload(self, mod):
        """ Ensure the add version page works when using a file upload. """
        new_mv = self.add_test_helper(mod, 'url_upload')
        verify_upload(new_mv)

    @slow_skip
    def test_edit_view_file_to_direct_link(self, mv):
        """ Ensure the edit version page is functional. """
        new_mv = self.edit_test_helper(mv, 'direct')
        verify_direct(new_mv)

    @slow_skip
    def test_edit_view_file_to_url_upload(self, mv):
        new_mv = self.edit_test_helper(mv, 'url_upload')
        verify_upload(new_mv)

    def test_delete_version_with_file(self, mv):
        """ Ensure delete version actually deletes the mod_file. """
        from gridfs import GridFS
        from mongoengine.connection import get_db
        # Create a variable for the mod_file and mod
        mf_id = mv.mod_file.grid_id
        mod = mv.mod
        # Create request to delete the new modversion
        request = match_request(id=mv.id)
        self.authenticate(mod.owner)
        # Run
        self.make_one(request).deleteversion()
        # Reload the mod again
        mod.reload()
        # Check if the version's gone
        assert not mod.versions
        # Check if the mod file has been deleted
        assert not GridFS(get_db(), collection='modfs').exists(mf_id)
