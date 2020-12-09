from datetime import datetime

from sherlock_back.api import db
from sherlock_back.api.controllers.cases import all_non_removed_cases_by_project

from sherlock_back.api.controllers.cycles import create_test_case_cycle, cycle_cases_by_project, last_cycle
from sherlock_back.api.controllers.projects import find_project, count_cycles_for_project
from sherlock_back.api.controllers.shared.cycle_project import count_cycle_stats
from sherlock_back.api.controllers.users import find_user
from sherlock_back.api.data.model import StateType, Cycle


def check_cycle_pre_condition(project_id):
    if find_project(id=project_id) and len(all_non_removed_cases_by_project(project_id)) > 0:
        return True
    return False

def project_details(project_id):
    """Fetch and return a PROJECT with parsed data from cycles."""
    project = find_project(project_id)
    project_last_cycle = last_cycle_data_parser(project_id)

    user = find_user(id=project['owner_id'])
    project.update({'owner_name': user['name']})
    project.update({'last_cycle': project_last_cycle})
    return project


def last_cycle_data_parser(project_id):
    project_last_cycle = last_cycle(project_id)
    details = {
        'cycle': None,
        'closed': None
    }

    if project_last_cycle:
        if project_last_cycle.state_code == StateType.closed:
            user_closed_by = find_user(id=project_last_cycle.closed_by)
            closed_by = user_closed_by.name

            closed_details = {
                'closed_at': datetime.strftime(project_last_cycle.closed_at, '%d-%m-%Y'),
                'closed_reason': project_last_cycle.closed_reason,
                'closed_by': closed_by,
            }
            details['closed'].update(closed_details)

        cycle_cases_h = cycle_cases_by_project(project_id)
        cycle_details = {
            'id': project_last_cycle.id,
            'state_code': project_last_cycle.state_code.value,
            'cycle': project_last_cycle.cycle,
            'created_at': datetime.strftime(project_last_cycle.created_at, '%d-%m-%Y'),
            'stats': count_cycle_stats(cycle_cases_h)
        }
        details['cycle'].update(cycle_details)
    return details


def create_cycle(project_id, cycle_name=None):
    """POST endpoint for new cycles.
    Param:
        {'cycle_name': required but can be empty }
    """

    project_last_cycle = last_cycle(project_id)
    if project_last_cycle and project_last_cycle.state_code == StateType.active:
        return False

    # fetch all project cycles
    cycle_number = count_cycles_for_project(project_id)
    cases = all_non_removed_cases_by_project(project_id)

    if len(cases) == 0:
        return False

    new_cycle = Cycle(
        cycle=cycle_number,
        name=cycle_name or "Cycle Number {}".format(cycle_number),
        project_id=project_id
    )
    db.session.add(new_cycle)
    db.session.commit()

    for case in cases:
        create_test_case_cycle(
            cycle_id=new_cycle.id,
            case_id=case.id,
            parent_id=case.parent_id
        )

    return new_cycle.id
