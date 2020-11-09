from sherlock_back.api.controllers.cases import all_non_removed_cases_by_scenario
from sherlock_back.api.controllers.cycles import fetch_cycle_scenario, fetch_cycle_cases
from sherlock_back.api.controllers.scenarios import find_scenarios
from sherlock_back.api.controllers.shared.cycle_scenarios import parse_cycle_scenario
from sherlock_back.api.controllers.tags import find_tags_by_case_id


def parse_test_cases_for_cycle(cycle_id, scenario_id):
    parsed_cases = []
    scenario = find_scenarios(id=scenario_id)
    parsed_scenario = parse_cycle_scenario(
        cycle_id=cycle_id,
        scenario_cycle_id=fetch_cycle_scenario(cycle_id=cycle_id, scenario_id=scenario_id),
        scenario_object=scenario
    )

    cycle_cases = fetch_cycle_cases(cycle_id)
    cases = all_non_removed_cases_by_scenario(scenario_id)
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
    parsed_scenario['cases'] = parsed_cases
    return parsed_scenario
