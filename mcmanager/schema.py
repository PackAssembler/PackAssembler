from functools import total_ordering
from mongoengine import *

# Mod targets
TARGETS = ('server', 'client', 'both')
# Minecraft versions
MCVERSIONS = ('1.5.2', '1.5.1', '1.5', '1.4.7')
# Forge version length
FV = 16


class User(Document):
    # Username, limited for formatting purposes
    username = StringField(required=True, min_length=6, max_length=32, unique=True)
    # Password, should be bcrypt hashed
    password = BinaryField(required=True)
    # Email, should be validated on client side first
    email = EmailField(required=True, unique=True)
    # Groups, used for authorization
    groups = ListField(StringField(), required=True)

    # Codes
    ## Activation code
    activate = IntField()
    ## Password reset code
    reset = IntField()


class ModVersion(Document):
    # Minecraft version
    mc_min = StringField(choices=MCVERSIONS, required=True)
    mc_max = StringField(choices=MCVERSIONS, required=True)
    # Minecraft Forge version
    ## If not defined, default to any version
    forge_min = StringField(max_length=FV)
    forge_max = StringField(max_length=FV)
    # Mod version and upload datetime
    version = StringField(required=True)
    # The file itself
    mod_file = FileField(required=True, collection_name='modfs')
    # Reference Mod ModVersion belongs to
    mod = ReferenceField('Mod', required=True)


@total_ordering
class Mod(Document):
    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def __eq__(self, other):
        return self.name == other.name
    # Information
    ## Name of mod
    name = StringField(required=True, max_length=32)
    ## Author(s) of the mod
    author = StringField(max_length=32)
    ## Where to download mod
    install = StringField(required=True, default="mods")
    ## Where to run mod (server, client, or both?)
    target = StringField(required=True, choices=TARGETS, default='both')
    ## Mod homepage
    url = URLField(required=True)
    ## Permission from author (unless uploader is the author)
    permission = StringField()
    # Versions of the mod (and compatibility information)
    versions = ListField(ReferenceField(ModVersion, reverse_delete_rule=PULL))
    # Owner: Full permissions
    owner = ReferenceField(User, required=True, reverse_delete_rule=NULLIFY)
    # Is outdated?
    outdated = BooleanField(required=True, default=False)

    meta = {
        'ordering': ['name']
    }


class PackBuild(Document):
    # Build number
    revision = IntField(required=True)
    # Build itself
    ## JSON File with information about mod versions included in package
    ## Should include all information except number
    build = StringField(required=True)
    # Configuration, should be on external server
    config = URLField()
    # Version information
    mc_version = StringField(required=True, choices=MCVERSIONS)
    forge_version = StringField(required=True, max_length=FV)
    # Reference Pack PackBuild belongs to
    pack = ReferenceField('Pack', required=True)


class Pack(Document):
    # Information
    name = StringField(required=True, max_length=32, unique=True)
    # Mod List
    mods = ListField(ReferenceField(Mod, reverse_delete_rule=DENY))
    # Builds
    builds = ListField(ReferenceField(PackBuild, reverse_delete_rule=PULL))
    # Latest PackBuild revision
    latest = IntField(required=True, default=0)
    # Owner of Pack
    owner = ReferenceField(User, required=True, reverse_delete_rule=NULLIFY)

    meta = {
        'ordering': ['name']
    }


class Server(Document):
    # Information
    name = StringField(required=True, max_length=32, unique=True)
    url = URLField()
    host = StringField(required=True)
    port = IntField(required=True)
    # Pack used
    build = ReferenceField('PackBuild', required=True, reverse_delete_rule=DENY)
    # Owner
    owner = ReferenceField(User, required=True, reverse_delete_rule=NULLIFY)
    # Configuration, should be on external server
    config = URLField()

    meta = {
        'ordering': ['name']
    }
