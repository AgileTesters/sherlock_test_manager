def check_first_run(db):    
    db.create_all()
    from sherlock_back.api.data.model import User

    user = User.query.filter_by(id=1).first()
    if user is None:
        initial_user = User(name='Admin',
                            email='admin@admin.xpto',
                            password='admin',
                            profile='admin')
        db.session.add(initial_user)
        db.session.commit()

