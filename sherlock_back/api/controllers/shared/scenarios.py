# from sherlock_back.api import db
# from sherlock_back.api.controllers.cases import all_non_removed_cases_by_scenario
# from sherlock_back.api.controllers.cycles import change_cycle_scenario_state
# from sherlock_back.api.controllers.shared.cycles import last_cycle
# from sherlock_back.api.controllers.tags import find_tags_by_case_id, get_all_scenario_tags
# from sherlock_back.api.data.model import StateType
#
#
# def mount_scenario_with_test_cases(scenario_id):
#     """Return Scenario and Cases."""
#
#     scenario = find_scenario(id=scenario_id)
#     test_cases = all_non_removed_cases_by_scenario(scenario_id=scenario_id)
#
#     # INJECT TAG INTO EACH TEST CASE
#     for case in test_cases:
#         case['tags'] = find_tags_by_case_id(case['id'])
#
#     return {
#         'scenario_id': scenario.id,
#         'scenario_state': scenario.state_code.value,
#         'scenario_name': scenario.name,
#         'cases': test_cases
#     }
#
#
# def change_status(scenario_id, action):
#     if action == 'DISABLE':
#         state = StateType.disable
#         cycle_state = StateType.blocked
#     elif action == 'ENABLE':
#         state = StateType.active
#         cycle_state = StateType.not_executed
#     elif action == 'REMOVE':
#         state = StateType.removed
#         cycle_state = StateType.removed
#
#     scenario_cases = find_scenarios(id=scenario_id)
#
#     # BULK ACTION
#     # ALL CHANGES TO SCENARIO STATE SHOULD PROPAGATE TO ITS TEST CASES STATE
#
#     scenario = find_scenario(id=scenario_id)
#     cycle = last_cycle(scenario.project_id)
#
#     scenario.state_code = state
#     db.session.add(scenario)
#     db.session.commit()
#     for case in scenario_cases:
#         case.state_code = state
#         db.session.add(case)
#         db.session.commit()
#
#     # CHANGE CYCLE SCENARIO STATE CODE + BULK FOR CYCLE TEST CASES RELATED TO THAT SCENARIO
#     if cycle and cycle.state_code != StateType.closed:
#         change_cycle_scenario_state(
#             cycle_state=cycle_state,
#             cycle_id=cycle.id,
#             scenario_id=scenario_id
#         )
#     return True
#
# def scenarios_by_project(project_id):
#     """Return Testcase Info."""
#     scenarios = find_scenarios(project_id=project_id)
#     for scenario in scenarios:
#         scenario['tags'] = get_all_scenario_tags(scenario_id=scenario['id'])
#     return scenarios
