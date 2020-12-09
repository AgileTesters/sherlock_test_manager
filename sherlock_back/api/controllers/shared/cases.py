from sherlock_back.api import db
from sherlock_back.api.controllers.cycles import create_test_case_cycle
from sherlock_back.api.controllers.shared.cycles import last_cycle
from sherlock_back.api.data.model import Case, StateType, EntityType


def create_test_case(test_case_text, parent_id, project_id, entity=EntityType.case):
    last_case = Case.query.filter_by(
        project_id=project_id).order_by(Case.order_index.desc()).first()

    if last_case:
        order_index = last_case.order_index + 1
    else:
        order_index = 0

    case = Case(
        name=test_case_text,
        parent_id=parent_id,
        project_id=project_id,
        entity=entity,
        order_index=order_index
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
