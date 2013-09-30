import requests
from sys import argv
from packassembler.schema import *

connect('mmltest')

d = requests.get('http://bot.notenoughmods.com/{0}.json'.format(argv[1])).json()

name_dict = {}
for mod in d:
    name = mod['name']
    del mod['name']
    name_dict[name] = mod
 
not_in = []

for mod in Mod.objects:
    if mod.versions:
        v = mod.versions[-1].version
    else:
        continue
    if mod.name in name_dict or mod.name.replace(' ', '') in name_dict:
        try:
            botv = name_dict[mod.name]['version']
        except KeyError:
            botv = name_dict[mod.name.replace(' ', '')]['version']
        if botv != v and botv != 'dev-only':
            print('{0:>20}{1:>16}{2:>16}'.format(mod.name, v, botv))
    else:
        not_in.append(mod.name)

print('\nNot in List\n' + '-' * 30)
for mod in not_in:
    print(mod)
print('Total:', len(not_in))
