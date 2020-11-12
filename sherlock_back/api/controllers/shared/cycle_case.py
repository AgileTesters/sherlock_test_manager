from sherlock_back.api.controllers.cases import all_non_removed_cases_by_project
from sherlock_back.api.controllers.cycles import fetch_cycle_cases
from sherlock_back.api.controllers.tags import find_tags_by_case_id


def parse_test_cases_for_cycle(cycle_id, project_id):
    parsed_cases = []
    parsed_cycle_data = {
        'cycle_id': cycle_id,
    }

    cycle_cases = fetch_cycle_cases(cycle_id)
    cases = all_non_removed_cases_by_project(project_id)
    for item in cycle_cases:
        for case in cases:
            if item.case_id == case.id:
                parsed_cases.append({
                    'case_name': case.name,
                    'case_id': case.id,
                    'case_cycle_id': item.id,
                    'case_cycle_state': item.state_code.value,
                    'tags': find_tags_by_case_id(case.id),
                })
                break
    parsed_cycle_data['cases'] = parsed_cases
    return parsed_cycle_data
