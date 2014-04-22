from datetime import datetime, timedelta
from packassembler.schema import *

connect('', host=input('DB URL: '))
too_old = datetime.now() - timedelta(days=45)

for user in User.objects:
    if not Mod.objects(owner=user) and user.group == 'user' and (not user.last_login or user.last_login < too_old):
        user.delete()
