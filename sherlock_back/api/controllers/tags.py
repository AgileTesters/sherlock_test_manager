
from sherlock_back.api import db
from sherlock_back.api.data.model import TagScenario, TagCase, TagCaseSchema, TagScenarioSchema


# SCENARIO TAGS

def create_scenario_tag(scenario_id, tag):
    new_tag = TagScenario(
        scenario_id=scenario_id,
        tag=tag)
    db.session.add(new_tag)
    db.session.commit()


def delete_scenario_tag(tag_id):
    tag = get_tag_scenario(tag_id)
    db.session.delete(tag)
    db.session.commit()


def get_tag_scenario(tag_id):
    return TagScenario.query.filter_by(id=tag_id).first()


def get_all_scenario_tags(scenario_id):
    scenario_tags_raw = TagScenario.query.filter_by(
            scenario_id=scenario_id).all()
    schema = TagScenarioSchema(many=True)
    return schema.dump(scenario_tags_raw).data


# TAG CASE

def find_tags_by_case_id(case_id):
    tag_cases = TagCase.query.filter_by(
        case_id=case_id).all()
    schema = TagCaseSchema(many=True)
    return schema.dump(tag_cases).data


def get_tag_case(tag_case_id):
    return TagCase.query.filter_by(id=tag_case_id).first()


def create_case_tag(case_id, tag):
    """
    Param:
        {
        'case_id': Int - required,
        'tag': String - required
        }
    """
    new_tag = TagCase(
        case_id=case_id,
        tag=tag)
    db.session.add(new_tag)
    db.session.commit()


def delete_case_tag(tag_id):
    tag = get_tag_scenario(tag_id)
    db.session.delete(tag)
    db.session.commit()
