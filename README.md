# marshmallow-metaclass

Meta class that uses marshmallow fields in creating objects.

### How to use

Just add `Meta` as a `metaclass`.

```
from marshmallow import fields
from mallows import Meta

User(metaclass=Meta):
    name = fields.Str()
```

### Example

```
from marshmallow import fields
from datetime import datetime

from mallows import Meta


class TitleStr(fields.Str):
    """Custom field"""

    def _deserialize(self, value, attr, obj, **kwargs):
        """This is used by the `schema.load`."""
        if value is None:
            return ''
        return str(value).title()


class Human(metaclass=Meta):
    name = TitleStr()  # use custom field
    birth_year = fields.Int()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # don't forget
        self.age = datetime.now().year - self.birth_year


class Singer(Human):
    grammy_awards = fields.Int()


class Album(metaclass=Meta):
    name = TitleStr()  # use custom field
    singer = fields.Nested(Singer.SCHEMA)  # use schema of `Singer`
    songs = fields.List(TitleStr())  # use custom field


lady = Singer(name='lady gaga', birth_year=1986, grammy_awards=12)
print(lady.age)
# 35
print(lady.data)
# {'grammy_awards': 12, 'birth_year': 1986, 'name': 'Lady Gaga'}

album = Album(
    name='chromatica',
    singer=lady.asdict(),  # or `lady.data` to make it less strict
    songs=['911', 'rain on me', 'plastic doll']
)
print(album.name)
# Chromatica
print(album.asdict())
# {
#     'singer': {'birth_year': 1986, 'grammy_awards': 12, 'name': 'Lady Gaga'},
#     'songs': ['911', 'Rain On Me', 'Plastic Doll'],
#     'name': 'Chromatica'
# }
```
