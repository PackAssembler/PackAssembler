from packassembler.schema import *
connect('mmltest')

for user in users:
    if not Mod.objects(owner=user) and not Pack.objects(owner=user) and not Server.objects(owner=user):
        user.delete()
