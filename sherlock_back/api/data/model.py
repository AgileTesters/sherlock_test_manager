"""Setup for SHERLOCK database."""
from datetime import datetime
from enum import Enum
import bcrypt

from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from sherlock_back.api import db, secret_key
from sherlock_back.api.db_init import check_first_run


class EntityType(Enum):
    case = "case"
    scenario = "scenario"
    describe = "describe"
    context = "context"
    feature = "feature"


class StateType(Enum):
    active = "active"
    disable = "disable"
    not_executed = "not_executed"
    passed = "passed"
    error = "error"
    blocked = "blocked"
    ongoing = "ongoing"
    closed = "closed"
    removed = "removed"


class Project(db.Model):
    __tablename__ = "project"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text(500), nullable=False)

    cases = db.relationship('Case', backref='project', lazy=True)
    cycles = db.relationship('Cycle', backref='project', lazy=True)

    def __init__(self, name, owner_id, description):
        """Setting params to the object."""
        self.name = name
        self.owner_id = owner_id
        self.description = description


class Case(db.Model):
    __tablename__ = "case"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(500), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    parent_id = db.Column(db.Integer, nullable=True)
    entity = db.Column(db.Enum(EntityType))
    state_code = db.Column(db.Enum(StateType))
    order_index = db.Column(db.Integer, nullable=False)

    cycle_cases = db.relationship('CycleCases')
    case = db.relationship('Project')

    def __init__(self, name, project_id, order_index, entity, parent_id=None):
        self.name = name
        self.project_id = project_id
        self.parent_id = parent_id
        self.entity = entity
        self.state_code = StateType.active
        self.order_index = order_index


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    profile = db.Column(db.String(50), nullable=False)

    project = db.relationship('Project')

    def __init__(self, name, email, password, profile='user'):
        self.name = name
        self.email = email
        self.password = User.generate_hash_password(password)
        self.profile = profile

    def verify_password(self, password):
        password = password.encode('utf-8')
        self.password = self.password.encode('utf-8')
        if bcrypt.hashpw(password, self.password) == self.password:
            return True
        return False

    @staticmethod
    def generate_hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token_and_return_user(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.query.get(data['id'])


class Cycle(db.Model):
    __tablename__ = "cycle"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cycle = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    state_code = db.Column(db.Enum(StateType))

    cycle_cases = db.relationship('CycleCases')

    created_at = db.Column(db.DateTime, default=datetime.now)
    closed_at = db.Column(db.DateTime)
    closed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    closed_reason = db.Column(db.String(250))
    last_change = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, cycle, name, project_id):
        self.cycle = cycle
        self.name = name
        self.project_id = project_id
        self.state_code = StateType.active


class CycleCases(db.Model):
    __tablename__ = "cycle_cases"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    state_code = db.Column(db.Enum(StateType))
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'))
    parent_id = db.Column(db.Integer, nullable=True)
    last_executed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_executed_at = db.Column(db.DateTime)

    def __init__(self, cycle_id, case_id, parent_id):
        """Setting params to the object."""
        self.cycle_id = cycle_id
        self.case_id = case_id
        self.parent_id = parent_id
        self.state_code = StateType.not_executed


class NotesCase(db.Model):
    __tablename__ = "notes_case"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cycle_id = db.Column(db.Integer, db.ForeignKey('cycle.id'))
    case_id = db.Column(db.Integer)
    text = db.Column(db.Text)

    def __init__(self, cycle_id, case_id, text):
        """Setting params to the object."""
        self.cycle_id = cycle_id
        self.case_id = case_id
        self.text = text


class TagCase(db.Model):
    __tablename__ = "tags_case"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer)
    tag = db.Column(db.String(250))

    def __init__(self, case_id, tag):
        self.case_id = case_id
        self.tag = tag


#  SCHEMAS #####


class TagCaseSchema(Schema):
    id = fields.Int(dump_only=True)
    case_id = fields.Int()
    tag = fields.Str()


class CycleSchema(Schema):
    id = fields.Int(dump_only=True)
    cycle = fields.Int()
    project_id = fields.Int()
    name = fields.Str()
    state_code = EnumField(StateType)
    created_at = fields.Str()
    closed_at = fields.Str()
    last_change = fields.Str()


class TestCaseSchema(Schema):
    id = fields.Int(dump_only=True)
    project_id = fields.Int()
    parent_id = fields.Int()
    name = fields.Str()
    order_index = fields.Int()
    state_code = EnumField(StateType)


class UsersSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    email = fields.Str()
    profile = fields.Str()


class ProjectSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    owner_id = fields.Int()
    description = fields.Str()


check_first_run(db)
