marshmallow-sqlalchemy-referential
============================================

Installation
++++++++++++

  pip install marshmallow-sqlalchemy-referential

Sample Usage
++++++++++++

.. code-block:: python

  import sqlalchemy as sa
  from sqlalchemy.ext.declarative import declarative_base
  from marshmallow_sqlalchemy_referential import Referential
  from marshmallow_sqlalchemy import ModelSchema
  from marshmallow import fields

  Base = declarative_base()

  user_group_assoc = sa.Table(
    'user_group_assoc', Base.metadata,
    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')),
    sa.Column('group_id', sa.Integer, sa.ForeignKey('group.id'))
  )

  class User(Base):
      __tablename__ = 'user'
      
      id = sa.Column(sa.Integer(), primary_key=True)
      groups = sa.orm.relationship('Group', secondary=user_group_assoc)

  class Group(Base):
      __tablename__ = 'group'

      id = sa.Column(sa.Integer(), primary_key=True)
      users = sa.orm.relationship('User', secondary=user_group_assoc)
  

  class GroupSchema(ModelSchema):
    class Meta():
        dump_only = ['id']

    id = fields.Integer()

  class UserSchema(ModelSchema):
    class Meta():
        dump_only = ['id']

    id = fields.Integer()
    groups = Referential(GroupSchema, model=Group, many=True)


  

