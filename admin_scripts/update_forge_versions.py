import requests
from packassembler.schema import *

connect('mmltest')

URL = 'http://files.minecraftforge.net/minecraftforge/json'
KEY = 'forgeversions'

raw_build_data = requests.get(URL).json()['builds']
build_data = {}

for build in raw_build_data:
    mc_version = build['files'][-1]['mcver'].replace('.', '_')
    forge_version = build['version']

    build_data.setdefault(mc_version, []).append(forge_version)

store = Setting.objects(key=KEY).first()
if store is None:
    store = Setting(key=KEY)

store.build_data = build_data
store.save()
