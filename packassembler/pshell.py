from packassembler.schema import connect

def setup(env):
    connect('', host=env['registry'].settings.get('mongodb', 'packassembler'))
