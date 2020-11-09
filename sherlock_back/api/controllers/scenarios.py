
from sherlock_back.api import db
from sherlock_back.api.data.model import ScenariosSchema, Scenario


def find_scenario(**kwargs):
    scenario = Scenario.query.filter_by(**kwargs).first()
    scenario_schema = ScenariosSchema(many=False)
    return scenario_schema.dump(scenario).data


def find_scenarios(**kwargs):
    scenario = Scenario.query.filter_by(**kwargs).all()
    scenario_schema = ScenariosSchema(many=False)
    return scenario_schema.dump(scenario).data


def edit_test_scenario(scenario_id, scenario_text):
    scenario = find_scenario(id=scenario_id)

    scenario.name = scenario_text
    db.session.add(scenario)
    db.session.commit()
