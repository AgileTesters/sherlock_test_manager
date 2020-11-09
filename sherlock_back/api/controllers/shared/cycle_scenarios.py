from sherlock_back.api import db
from sherlock_back.api.controllers.cycles import fetch_cycle_cases, find_cycle_scenarios
from sherlock_back.api.controllers.projects import find_project
from sherlock_back.api.controllers.scenarios import find_scenarios
from sherlock_back.api.controllers.shared.cycle_project import count_cycle_stats
from sherlock_back.api.controllers.shared.cycles import last_cycle
from sherlock_back.api.controllers.tags import get_all_scenario_tags
from sherlock_back.api.data.model import CycleScenarios, Scenario


def create_test_scenario(scenario_text, project_id):
    if not find_project(project_id):
        return False

    new_scenario = Scenario(name=scenario_text, project_id=project_id)
    db.session.add(new_scenario)
    db.session.commit()

    cycle = last_cycle(project_id)
    if cycle:
        create_scenario_cycle(cycle_id=cycle.id, scenario_id=new_scenario.id)


def create_scenario_cycle(cycle_id, scenario_id):
    scenario_cycle = CycleScenarios(
        cycle_id=cycle_id,
        scenario_id=scenario_id
    )
    db.session.add(scenario_cycle)
    db.session.commit()


def parse_cycle_scenario(cycle_id, scenario_cycle_id, scenario_object):
    cases = fetch_cycle_cases(cycle_id=cycle_id)
    return {
        'scenario_name': scenario_object.name,
        'scenario_id': scenario_object.id,
        'scenario_cycle_id': scenario_cycle_id,
        'cases_stats': count_cycle_stats(cases),
        'tags': get_all_scenario_tags(scenario_id=scenario_object.id),
    }


def parse_scenarios_for_cycle(project_id, cycle_id):
    cycle_scenarios = find_cycle_scenarios(cycle_id)
    scenarios = find_scenarios(project_id=project_id)

    parsed_scenarios = []
    for item in cycle_scenarios:
        for scenario in scenarios:
            if scenario.id == item.scenario_id:
                parsed_scenarios.append(parse_cycle_scenario(
                    cycle_id=cycle_id,
                    scenario_cycle_id=item.id,
                    scenario_object=scenario
                ))
                break

