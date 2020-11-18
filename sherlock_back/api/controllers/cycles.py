"""Sherlock Cycles Controllers."""
from datetime import datetime

from sherlock_back.api import db
from sherlock_back.api.controllers.shared.cycle_project import count_cycle_stats
from sherlock_back.api.data.model import (Cycle, CycleCases, StateType)

# CYCLE


def find_cycle(**kwargs):
    return Cycle.query.filter_by(**kwargs).first()


def last_cycle(project_id):
    return Cycle.query.filter_by(project_id=project_id).order_by('id').first()


def cycle_cases_by_project(project_id):
    return Cycle.query.filter_by(project_id=project_id).all()


# CYCLE - TEST CASE

def create_test_case_cycle(cycle_id, case_id, parent_id=None):
    cycle_case = CycleCases(cycle_id=cycle_id,
                            case_id=case_id,
                            parent_id=parent_id)
    db.session.add(cycle_case)
    db.session.commit()


def fetch_cycle_cases(cycle_id):
    return CycleCases.query.filter_by(cycle_id=cycle_id).all()


def find_cycle_case(cycle_id, case_id):
    return CycleCases.query.filter_by(cycle_id=cycle_id).filter_by(case_id=case_id).first()


def delete_cycle_case(cycle_case_id):
    cycle_case = CycleCases.query.filter_by(id=cycle_case_id).first()
    db.session.delete(cycle_case)
    db.session.commit()

# CYCLE - PROJECT


def find_project_cycles(project_id, cycle_limit):
    """
        In case of limit = 0, Remove the limit
    """
    cycles = Cycle.query.filter_by(
        project_id=project_id).order_by(
        Cycle.id.desc())
    if cycle_limit > 0:
        cycles = cycles.limit(cycle_limit).all()
    return cycles.all()

# TODO: METHOD TO BULK CHANGE STUFF ---> REFACTOR WITH ENTITY
# def change_cycle_scenario_state(cycle_state, cycle_id, scenario_id):
#     # blocking scenario on active current_cycle
#     cycle_scenario = fetch_cycle_scenario(cycle_id=cycle_id, scenario_id=scenario_id)
#     cycle_scenario.state_code = cycle_state
#     db.session.add(cycle_scenario)
#     db.session.commit()
#
#     # BULK STATE CHANGE FOR CYCLE TEST CASES RELATED TO THAT SCENARIO
#     cycle_cases = cycle_cases_by_scenario(cycle_id=cycle_id, scenario_id=scenario_id)
#     for case in cycle_cases:
#         case.state_code = cycle_state
#         db.session.add(case)
#         db.session.commit()


def cycle_timeline_resume_by_project(project_id, cycle_limit):
    # TODO: Need to find a better way - Did this cz chartist works like that.
    # TODO: Find another chart that handle better dicts

    last_project_cycles = find_project_cycles(project_id, cycle_limit)

    cycles = []
    cycle_cases_passed = []
    cycle_cases_failed = []
    cycle_cases_blocked = []
    cycle_cases_not_executed = []

    for item in reversed(last_project_cycles):
        cycle_cases = fetch_cycle_cases(item.id)

        # Its possible to have a Cycle Nickname
        if item.cycle == last_project_cycles[0].cycle:
            cycles.append('[Current] ' + item.name)
        else:
            cycles.append(item.name)

        # Chartist only understand one array por category (passed, error, etc)
        # Created an array for each category based on the cycle history
        stats = count_cycle_stats(cycle_cases)
        cycle_cases_passed.append(stats['total_passed'])
        cycle_cases_failed.append(stats['total_error'])
        cycle_cases_blocked.append(stats['total_blocked'])
        cycle_cases_not_executed.append(stats['total_not_executed'])

    return {
        'cycles_number': cycles,
        'cycles_passed': cycle_cases_passed,
        'cycles_failed': cycle_cases_failed,
        'cycles_blocked': cycle_cases_blocked,
        'cycles_not_executed': cycle_cases_not_executed
    }


def get_cycle_case_stats(cycle_id):
    cycle_cases_h = fetch_cycle_cases(cycle_id)
    return count_cycle_stats(cycle_cases_h)


def close_cycle(cycle_id, reason, user_id):
    # TODO: Check untested cases. # TODO: Remember the previous TODO hue HUE

    cycle = find_cycle(id=cycle_id)
    if cycle.state_code != StateType.closed:
        cycle.closed_reason = reason
        cycle.closed_by = user_id
        cycle.state_code = StateType.closed
        cycle.closed_at = datetime.now()
        cycle.last_change = datetime.now()
        db.session.add(cycle)
        db.session.commit()
    return True


def change_cycle_case_state_code(action, cycle_id, case_id):
    case = find_cycle_case(cycle_id=cycle_id, case_id=case_id)

    if case:
        case.state_code = StateType[action]
        db.session.add(case)
        db.session.commit()
        return True
    return False
