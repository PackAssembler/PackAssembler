from functools import total_ordering
from mongoengine import *

# Mod targets
TARGETS = ('server', 'client', 'both')
# Minecraft versions
MCVERSIONS = ('1.6.2', '1.5.2', '1.5.1', '1.5', '1.4.7')
# Forge version length
FV = 16


class User(Document):
    # Username, limited for formatting purposes
    username = StringField(required=True, min_length=6, max_length=32, unique=True)
    # Password, should be bcrypt hashed
    password = BinaryField(required=True)
    # Email, should be validated on client side first
    email = EmailField(required=True, unique=True)
    # Group, used for authorization
    group = StringField(required=True, default='user')
    # Avatar
    avatar_type = IntField(default=0)
    email_hash = StringField(default='')

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
    mod_file = FileField(collection_name='modfs')
    mod_file_url = URLField()
    # Reference Mod ModVersion belongs to
    mod = ReferenceField('Mod', required=True)


@total_ordering
class Mod(Document):
    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def __eq__(self, other):
        try:
            return self.name == other.name
        except AttributeError:
            return False

    # Information
    ## Name of mod
    name = StringField(required=True, max_length=32, unique=True)
    ## Readable id
    rid = StringField()
    ## Description of mod
    description = StringField()
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
    owner = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    # Is outdated?
    outdated = BooleanField(required=True, default=False)
    # Formatting extras
    banner = URLField()

    meta = {
        'ordering': ['name']
    }

Mod.register_delete_rule(ModVersion, 'mod', CASCADE)


class PackBuild(Document):
    # Build number
    revision = IntField(required=True)
    # Mod versoins
    mod_versions = ListField(ReferenceField(ModVersion))
    # Configuration, should be on external server
    config = URLField()
    # Version information
    mc_version = StringField(required=True, choices=MCVERSIONS)
    forge_version = StringField(required=True, max_length=FV)
    # Reference Pack PackBuild belongs to
    pack = ReferenceField('Pack', required=True)


class Pack(Document):
    # Information
    name = StringField(required=True, unique=True)
    # Readable id
    rid = StringField(required=True)
    # Mod List
    mods = ListField(ReferenceField(Mod, reverse_delete_rule=DENY))
    # Builds
    builds = ListField(ReferenceField(PackBuild, reverse_delete_rule=PULL))
    # Latest PackBuild revision
    latest = IntField(required=True, default=0)
    # Owner of Pack
    owner = ReferenceField(User, required=True, reverse_delete_rule=DENY)

    meta = {
        'ordering': ['name']
    }

Pack.register_delete_rule(PackBuild, 'pack', CASCADE)


class Server(Document):
    # Information
    name = StringField(required=True, max_length=32, unique=True)
    url = URLField()
    host = StringField(required=True)
    port = IntField(required=True)
    # Readable id
    rid = StringField()
    # Pack used
    build = ReferenceField('PackBuild', required=True, reverse_delete_rule=DENY)
    # Owner
    owner = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    # Configuration, should be on external server
    config = URLField()

    meta = {
        'ordering': ['name']
    }
