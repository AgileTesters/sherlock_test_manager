"""Sherlock Project Controllers"""

from sherlock_back.api import db
from sherlock_back.api.controllers.cycles import find_project_cycles
from sherlock_back.api.controllers.users import find_user
from sherlock_back.api.data.model import Project, ProjectSchema


def get_all_projects():
    projects = Project.query.all()
    project_schema = ProjectSchema(many=True)
    return project_schema.dump(projects)


def find_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    project_schema = ProjectSchema(many=False)
    return project_schema.dump(project)


def project_owner_parser(project_id):
    project = find_project(project_id)
    return find_user(id=project['owner_id'])


def create_project(name, owner_id, description):
    new_project = Project(
        name=name,
        description=description,
        owner_id=int(owner_id),
    )
    db.session.add(new_project)
    db.session.commit()
    return new_project


def edit_project(project_id, project_payload):
    project_changes = dict(project_payload)

    project_data = Project.query.filter(Project.id == project_id).update(project_changes)
    db.session.add(project_data)
    db.session.commit()


def count_cycles_for_project(project_id):
    all_project_cycles = find_project_cycles(project_id=project_id, cycle_limit=0)
    return len(all_project_cycles)
