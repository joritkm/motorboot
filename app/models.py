from app import db, config
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate


not_empty = validate.Length(min=1, error='Field cannot be empty')


class CRUD():

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class Host(db.Model, CRUD):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer(), primary_key=True)
    hostname = db.Column(db.String(64), nullable=False, unique=True)
    hwaddress = db.Column(db.String(64), nullable=False, unique=True)
    target_id = db.Column(db.Integer(), db.ForeignKey('boottargets.id'))
    target = db.relationship('Boottarget', backref='used_by')

    def __init__(self,hostname,hwaddress):
        self.hostname = hostname
        self.hwaddress = hwaddress


class Boottarget(db.Model, CRUD):
    __tablename__ = 'boottargets'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)


class BoottargetSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=not_empty)

    class Meta:
        type_ = 'boottarget'


class HostSchema(Schema):
    id = fields.Integer(dump_only=True)
    hostname = fields.String(validate=not_empty)
    hwaddress = fields.String(validate=not_empty)
    target = fields.String()

    class Meta:
        type_ = 'host'
