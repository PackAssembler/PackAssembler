from mongoengine import *
from datetime import datetime

# Mod targets
TARGETS = ('server', 'client', 'both')
# Minecraft versions
MCVERSIONS = ('1.4.7', '1.5', '1.5.1', '1.5.2')
# Minecraft version length
MCV = 8
# Forge version length
FV = 16


class User(Document):
    # Username, limited for formatting purposes
    username = StringField(required=True, min_length=6, max_length=32, unique=True)
    # Password, should be bcrypt hashed
    password = BinaryField(required=True)
    # Email, should be validated on client side first
    email = EmailField(required=True)
    # Groups, used for authorization
    groups = ListField(StringField(), required=True)


class ModVersion(Document):
    # Minecraft version
    mc_min = StringField(choices=MCVERSIONS, required=True)
    mc_max = StringField(max_length=MCV, required=True)
    # Minecraft Forge version
    ## If not defined, default to any version
    forge_min = StringField(max_length=FV)
    forge_max = StringField(max_length=FV)
    # Mod version and upload datetime
    version = StringField(required=True)
    upload_date = DateTimeField(required=True, default=datetime.now)
    # The file itself
    mod_file = FileField(required=True, collection_name='modfs')
    # Reference Mod ModVersion belongs to
    mod = ReferenceField('Mod', required=True)


class Mod(Document):
    # Information
    ## Name of mod
    name = StringField(required=True, max_length=32)
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


class PackBuild(Document):
    # Date build added
    build_date = DateTimeField(required=True, default=datetime.now)
    # Build number
    revision = IntField(required=True)
    # Build itself
    ## JSON File with information about mod versions included in package
    ## Should include all information except build date
    build = StringField(required=True)
    # Configuration, should be on external server
    config = URLField()
    # Version information
    mc_version = StringField(required=True, max_length=MCV)
    forge_version = StringField(required=True, max_length=FV)
    # Reference Pack PackBuild belongs to
    pack = ReferenceField('Pack', required=True)


class Pack(Document):
    # Information
    name = StringField(required=True, max_length=32)
    # Mod List
    mods = ListField(ReferenceField(Mod, reverse_delete_rule=PULL))
    # Builds
    builds = ListField(ReferenceField(PackBuild))
    # Owner of Pack
    owner = ReferenceField(User, required=True, reverse_delete_rule=NULLIFY)
