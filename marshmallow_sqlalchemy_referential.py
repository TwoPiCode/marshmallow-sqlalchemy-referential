from marshmallow_sqlalchemy.fields import get_schema_for_field
from marshmallow import fields, Schema, ValidationError


class Referential(fields.Field):
    def __init__(self, related_schema, model=None, many=False, key='id',
                 key_field=None, **kwargs):
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
                {"id": 1},
                {"id": 2}
            ]
        }

        """

        super().__init__(many=many, **kwargs)

        if key_field is None:
            self._key = key
            key_field = fields.Integer(load_from=key, required=True)
        else:
            self._key = '_key'

        class ReferentialLoader(Schema):
            key = key_field

        self._related_schema = related_schema
        self._model = model
        self._many = many
        self._loader = ReferentialLoader(many=self._many)

        if hasattr(self._related_schema, '__name__'):
            self._related_schema = self._related_schema(many=self._many)

    @property
    def session(self):
        schema = get_schema_for_field(self)
        return schema.session

    def _serialize(self, value, attr, obj):
        data, err = self._related_schema.dump(value)
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
                            self._key: "Record could not be found"
                        }
                    }
                    raise ValidationError(err)
                rv.append(item)

            return rv
        else:
            return "Not Implemented"
