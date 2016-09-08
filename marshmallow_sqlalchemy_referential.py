from marshmallow_sqlalchemy.fields import get_schema_for_field
from marshmallow import fields, Schema, ValidationError, class_registry
from marshmallow.compat import basestring
from marshmallow.base import SchemaABC


class Referential(fields.Field):

    """A marshmallow-sqlalchemy field allows referential CRUD on relational fields.

    :param related_schema: The schema to serialise the field values
    :param model: The model queried when de-serializing
    :param many: `True` if this is a collection (default `False`)
    :param key: The key field name when loading (default `id`)
    :param key_field: The key field (marshmallow.fields.Field) used when
                      loading. Overrides `key`

`
    For example, on a one to many relationship, on the many side, you may
    want to set the list of related entities.

    To do so, you would specify:

    {
        "myRelatedField": [
            {"id": 1},
            {"id": 2}
        ]
    }

    And be returned a response which resolves to the actual objects:

    {
        "myRelatedField": [
            {
                "id": 1
                "name": "foo"
            },
            {
                "id": 2
                "name": "bar"
            }
        ]
    }

    """

    def __init__(self, nested, model=None, many=False, key='id',
                 exclude=tuple(), only=None, key_field=None, **kwargs):

        super().__init__(many=many, **kwargs)

        if key_field is None:
            self._key = key
            key_field = fields.Integer(load_from=key, required=True)
        else:
            self._key = '_key'

        class ReferentialLoader(Schema):
            key = key_field

        self._nested = nested
        self._model = model

        self._many = many
        self._only = only
        self._exclude = exclude

        self._loader = ReferentialLoader(many=self._many)

        self.__schema = None  # Cached Schema instance

    @property
    def schema(self):
        context = getattr(self.parent, 'context', {})

        if isinstance(self._only, basestring):
            only = (self._only, )
        else:
            only = self._only

        if not self.__schema:
            if isinstance(self._nested, SchemaABC):
                self.__schema = self._nested
                self.__schema.context.update(context)
            elif isinstance(self._nested, type) and \
                    issubclass(self._nested, SchemaABC):
                self.__schema = self._nested(many=self._many, only=only,
                                             exclude=self._exclude,
                                             context=context)

            elif isinstance(self._nested, basestring):
                if self._nested == fields._RECURSIVE_NESTED:
                    parent_class = self.parent.__class__
                    self.__schema = parent_class(
                        many=self._many, only=only, exclude=self._exclude,
                        context=context)
                else:
                    schema_class = class_registry.get_class(self._nested)
                    self.__schema = schema_class(
                        many=self._many, only=only, exclude=self._exclude,
                        context=context)
            else:
                raise ValueError('Nested fields must be passed a '
                                 'Schema, not {0}.'.format(
                                    self._nested.__class__))

        return self.__schema

    @property
    def session(self):
        schema = get_schema_for_field(self)
        return schema.session

    def _serialize(self, value, attr, obj):
        if value is None:
            return value

        data, err = self.schema.dump(value)
        return data

    def _deserialize(self, value, *args, **kwargs):
        data, err = self._loader.load(value)
        if err:
            raise ValidationError(err)

        if self._many:
            rv = []
            for i, elem in enumerate(data):
                item = self.session.query(self._model).get(elem['key'])
                if item is None:
                    err = {
                        i: {
                            self._key: "Record with {}='{}' could not be"
                                       " found".format(self._key,
                                                       repr(elem['key']))
                        }
                    }
                    raise ValidationError(err)
                rv.append(item)

            return rv
        else:
            item = self.session.query(self._model).get(data['key'])
            if item is None:
                err = {
                    self._key: "Record with {}={} could not be"
                               " found".format(self._key, repr(data['key']))
                }
                raise ValidationError(err)
            return item
