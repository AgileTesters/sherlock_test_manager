from datetime import datetime

from sherlock_back.api import db
from sherlock_back.api.controllers.cases import active_cases_by_project
from sherlock_back.api.controllers.cycles import create_test_case_cycle, cycle_cases_by_project, last_cycle
from sherlock_back.api.controllers.projects import find_project
from sherlock_back.api.controllers.scenarios import find_scenarios
from sherlock_back.api.controllers.shared.cycle_project import count_cycle_stats, count_cycles_for_project
from sherlock_back.api.controllers.shared.cycle_scenarios import create_scenario_cycle
from sherlock_back.api.controllers.users import find_user
from sherlock_back.api.data.model import StateType, Cycle


def check_cycle_pre_condition(project_id):
    eligible = {
        'have_scenarios': False,
        'have_active_cases': False,
    }

    if find_project({'id': project_id}):
        eligible['have_scenarios'] = True
        if len(active_cases_by_project(project_id)) > 0:
            eligible['have_active_cases'] = True
    return eligible


def last_cycle_data_parser(project_id):
    project_last_cycle = last_cycle(project_id)
    cycles = {
        'have_cycles': False,
        'last_cycle': None
    }

    if project_last_cycle:
        cycles['have_cycles'] = True

        if project_last_cycle.state_code == StateType.closed:
            user_closed_by = find_user(id=project_last_cycle.closed_by)
            closed_by = user_closed_by.name

            closed_details = {
                'closed_at': datetime.strftime(project_last_cycle.closed_at, '%d-%m-%Y'),
                'closed_reason': project_last_cycle.closed_reason,
                'closed_by': closed_by,
            }
            cycles.update(closed_details)

        cycle_cases_h = cycle_cases_by_project(project_id)
        cycle_details = {
            'id': project_last_cycle.id,
            'state_code': project_last_cycle.state_code.value,
            'cycle': project_last_cycle.cycle,
            'created_at': datetime.strftime(project_last_cycle.created_at, '%d-%m-%Y'),
            'stats': count_cycle_stats(cycle_cases_h)
        }
        cycles.update(cycle_details)
    return cycles


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
    cases = active_cases_by_project(project_id)

    if len(cases) == 0:
        return False

    new_cycle = Cycle(
        cycle=cycle_number,
        name=cycle_name or "Cycle Number {}".format(cycle_number),
        project_id=project_id
    )
    db.session.add(new_cycle)
    db.session.commit()

    # Create CYCLE Scenarios and Cases for the new cycle
    for scenario in find_scenarios(project_id=project_id):
        create_scenario_cycle(cycle_id=new_cycle.id, scenario_id=scenario.id)
    for case in cases:
        create_test_case_cycle(cycle_id=new_cycle.id, case_id=case.id, scenario_id=case.scenario_id)

    return new_cycle.id
