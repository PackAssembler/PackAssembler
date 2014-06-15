import uuid
import pytest
import packassembler.schema as db

# Settings
DB_NAME = str(uuid.uuid1())
DB_HOST = 'localhost'
DB_PORT = 27017


@pytest.fixture(scope="session", autouse=True)
def mongoengine_setup(request):
    d = db.connect(DB_NAME, host=DB_HOST, port=DB_PORT)

    def fin():
        d.drop_database(DB_NAME)
    request.addfinalizer(fin)
