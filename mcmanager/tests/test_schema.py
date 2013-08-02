from mmlserver.schema import *
from pymongo import MongoClient
from mongoengine.errors import *

MongoClient().drop_database('testdb')
connect('testdb')


def test_user_create():
    testuser = User(username='testuser',
                    password=b'password',
                    email='someemail@example.com',
                    groups=['group:user'])
    testuser.save()
    user = User.objects.first()
    assert user.username == testuser.username
    assert user.password == testuser.password
    assert user.email == testuser.email
    assert user.groups[0] == testuser.groups[0]
    testuser.delete()
    assert User.objects.first() is None


def test_mod_create():
    from datetime import datetime
    from os.path import dirname
    # Create fake owner
    test_user = User().save(validate=False)
    # Create embedded document
    mv = ModVersion(mc_min='1.5.2',
                    mc_max='1.5.2',
                    version='1.0')
    dname = dirname(__file__)
    if dname == "":
        dname = "."
    mv.mod_file.put(open(dname + '/test.zip', 'rb'))
    # Create actual document object
    mod = Mod(name='TestMod',
              versions=[mv],
              owner=test_user).save()
    # Testing
    mtest = Mod.objects.first()
    assert mtest.name == mod.name
    assert mtest.versions[0].version == mv.version
    assert mtest.versions[0].upload_date < datetime.now()
    assert mtest.owner == test_user
    # Clean
    mod.versions[0].mod_file.delete()
    mod.delete()
    assert Mod.objects.first() is None
    test_user.delete()


def test_modpack_create():
    from time import sleep
    # Initialize
    # Create fake owner
    test_user = User().save(validate=False)
    # Create fake mods
    mod1 = Mod().save(validate=False)
    mod2 = Mod().save(validate=False)
    # Create embedded build
    common_build = {'build': '{}',
                    'config': 'http://somesite.com/somepack.zip',
                    'mc_version': '1.5.2'}
    build1 = PackBuild(forge_version='7.8.0.712', **common_build)
    sleep(0.001)
    build2 = PackBuild(forge_version='7.8.0.713', **common_build)
    sleep(0.001)
    build3 = PackBuild(forge_version='7.8.0.714', **common_build)
    # Create modpack
    pack = Pack(name='TestPack',
                mods=[mod1, mod2],
                owner=test_user)
    pack.builds.append(build2)
    pack.builds.append(build3)
    pack.builds.append(build1)
    pack.save()
    # Testing
    packtest = Pack.objects.first()
    assert packtest.name == pack.name
    assert packtest.owner == test_user
    builds = sorted(list(packtest.builds), reverse=True)
    assert builds[0]['forge_version'] == build3['forge_version']
    assert builds[1]['forge_version'] == build2['forge_version']
    assert builds[-1]['forge_version'] == build1['forge_version']
    assert packtest.mods == pack.mods
    # Clean
    pack.delete()
    assert Pack.objects.first() is None
    test_user.delete()
    mod1.delete()
    mod2.delete()
