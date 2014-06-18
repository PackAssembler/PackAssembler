from factory.mongoengine import MongoEngineFactory
from packassembler import schema, security
from functools import partial
import factory


def numbered(base, n):
    return base + str(n)


class UserFactory(MongoEngineFactory):
    FACTORY_FOR = schema.User

    username = factory.Sequence(partial(numbered, 'SomeUser'))
    password = security.password_hash('secret')
    email = factory.LazyAttribute(lambda obj: obj.username + '@example.com')
    group = 'user'


class ContributorFactory(UserFactory):
    group = 'contributor'


class PackFactory(MongoEngineFactory):
    FACTORY_FOR = schema.Pack

    name = factory.Sequence(partial(numbered, 'Pack'))
    rid = factory.Sequence(partial(numbered, 'pack'))
    owner = factory.SubFactory(UserFactory)


class ModFactory(MongoEngineFactory):
    FACTORY_FOR = schema.Mod

    name = factory.Sequence(partial(numbered, 'Mod'))
    rid = factory.Sequence(partial(numbered, 'pack'))
    url = "http://www.example.com/"
    outdated = False
    owner = factory.SubFactory(UserFactory)
    author = 'SomeAuthor'
