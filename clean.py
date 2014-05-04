from pyramid.paster import bootstrap
from datetime import datetime, timedelta
from packassembler.schema import *
from sys import argv

env = bootstrap(argv[1])
connect('', host=env['registry'].settings.get('mongodb', 'packassembler'))
too_old = datetime.now() - timedelta(days=45)

for user in User.objects:
    if not Mod.objects(owner=user) and user.group == 'user' and (not user.last_login or user.last_login < too_old) and user.username != 'Orphan':
        user.delete()
