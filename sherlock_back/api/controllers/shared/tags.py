from sherlock_back.api.controllers.tags import create_scenario_tag, delete_scenario_tag


def register_scenario_tag(scenario_id, tag_string):
    return create_scenario_tag(scenario_id, tag_string)


def remove_scenario_tag(tag_id):
    return delete_scenario_tag(tag_id)
