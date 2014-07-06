from sys import argv
if len(argv) != 3:
    print("Usage: check.py config.ini mc-version")

import re
import requests
from packassembler.schema import *
from pyramid.paster import bootstrap

env = bootstrap(argv[1])
connect('', host=env['registry'].settings.get('mongodb', 'packassembler'))

d = requests.get('http://bot.notenoughmods.com/{0}.json'.format(argv[2])).json()

name_dict = {}
clean_regex = re.compile("[!@#$-']")
for mod in d:
    name = clean_regex.sub('', mod['name'].lower())
    del mod['name']
    name_dict[name] = mod

not_in = []

for mod in Mod.objects(versions__in=ModVersion.objects(mc_version=argv[2])):
    if mod.versions:
        v = mod.versions[-1].version
    else:
        continue
    mod_name = mod.name.lower()
    if not mod.outdated:
        if mod_name in name_dict or mod_name.replace(' ', '') in name_dict:
            try:
                botv = name_dict[mod_name]['version']
            except KeyError:
                botv = name_dict[mod_name.replace(' ', '')]['version']
            if botv != v and botv != 'dev-only':
                print('{0:>25}{1:>16}{2:>16}'.format(mod.name, v, botv))
                if input('Set outdated? ').lower() == 'y':
                    mod.outdated = True
                    mod.save()
        else:
            not_in.append(mod.name)

print('\nNot in List\n' + '-' * 30)
for mod in not_in:
    print(mod)
print('Total:', len(not_in))
