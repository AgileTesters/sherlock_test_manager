from sherlock_back.api import db
from sherlock_back.api.controllers.cycles import create_test_case_cycle
from sherlock_back.api.controllers.shared.cycles import last_cycle
from sherlock_back.api.data.model import Case, StateType


def create_test_case(test_case_text, parent_id, project_id, entity):
    case = Case(
        name=test_case_text,
        parent_id=parent_id,
        project_id=project_id,
        entity = entity
    )
    db.session.add(case)
    db.session.commit()

    # UPDATE ONGOING CYCLE
    cycle = last_cycle(case.project_id)
    if cycle and cycle.state_code != StateType.closed:
        create_test_case_cycle(
            cycle_id=cycle.id,
            case_id=case.id,
            parent_id=case.parent_id
        )
