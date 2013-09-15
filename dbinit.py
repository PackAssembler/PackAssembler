"""
Creates the orphan user.
"""
from mcmanager.security import password_hash
from mcmanager.schema import User, connect
from sys import argv


try:
    connect(argv[1])
    User(username='Orphan', password=password_hash(argv[2]), email=argv[3],
         groups='orphan').save(validate=False)
except IndexError:
    print('usage: {0} db orphan_password orphan_email'.format(argv[0]))
