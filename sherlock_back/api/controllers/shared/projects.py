from sherlock_back.api.controllers.projects import find_project
from sherlock_back.api.controllers.shared.cycles import last_cycle_data_parser


def project_details(project_id):
    """Fetch and return a PROJECT with parsed data from cycles."""
    project = find_project(project_id)
    project_last_cycle = last_cycle_data_parser(project_id)
    user = find_project(id=project.owner_id)
    project.update({'owner_name': user.name})
    project.update({'last_cycle': project_last_cycle})

    return project
