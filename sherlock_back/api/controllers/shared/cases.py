from sherlock_back.api import db
from sherlock_back.api.controllers.cycles import create_test_case_cycle
from sherlock_back.api.controllers.scenarios import find_scenario
from sherlock_back.api.controllers.shared.cycles import last_cycle
from sherlock_back.api.data.model import Case, StateType


def create_test_case(scenario_id, test_case_text):
    scenario = find_scenario(id=scenario_id)
    case = Case(
        name=test_case_text,
        scenario_id=scenario.id
    )
    db.session.add(case)
    db.session.commit()

    # UPDATE ONGOING CYCLE
    cycle = last_cycle(scenario.project_id)
    if cycle and cycle.state_code != StateType.closed:
        create_test_case_cycle(
            cycle_id=cycle.id,
            case_id=case.id,
            scenario_id=case.scenario_id
        )
