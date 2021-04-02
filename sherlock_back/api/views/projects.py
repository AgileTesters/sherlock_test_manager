"""Sherlock Project Controllers and Routes."""
from flask import Blueprint, request, jsonify, make_response, g

from sherlock_back.api import auth
from sherlock_back.api.controllers.projects import create_project, edit_project
from sherlock_back.api.controllers.shared.cycles import project_details
from sherlock_back.api.helpers.string_operations import safe_fetch_content

project = Blueprint('projects', __name__)


@project.route('/project/<int:project_id>', methods=['GET'])
@auth.login_required
def get_project_details(project_id):
    """Show Project Details and last cycle Details."""
    project_with_details = project_details(project_id)
    return make_response(jsonify(project_with_details))


@project.route('/new', methods=['POST'])
@auth.login_required
def new():
    """POST endpoint for new projects.

    Param:
         {
            name: required,
            description: required
         }
    """
    import pdb
    pdb.set_trace()

    name = safe_fetch_content(request, 'name')
    description = safe_fetch_content(request, 'description')

    new_project = create_project(
        name=name,
        owner_id=int(g.user.id),
        description=description
    )

    return make_response(jsonify(message='PROJECT_CREATED', project_id=new_project.id))


@project.route('/project/<int:project_id>/edit/', methods=['POST'])
@auth.login_required
def edit_project_endpoint(project_id):
    """POST endpoint for editing existing users."""
    edit_project(project_id, request.get_json())
    return make_response(jsonify(message='PROJECT_EDITED'))
