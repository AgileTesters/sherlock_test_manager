
from sherlock_back.api import db
from sherlock_back.api.data.model import TagCase, TagCaseSchema


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
    tag = find_tags_by_case_id(tag_id)
    db.session.delete(tag)
    db.session.commit()
