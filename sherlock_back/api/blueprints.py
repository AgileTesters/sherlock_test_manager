def register_blue_prints(app):
    from sherlock_back.api.views.users import users
    from sherlock_back.api.views.projects import project
    from sherlock_back.api.views.dashboard import dashboard
    from sherlock_back.api.views.testcases import test_cases
    from sherlock_back.api.views.cycles import cycles

    app.register_blueprint(dashboard, url_prefix='/api/dashboard')
    app.register_blueprint(users, url_prefix='/api/users')
    app.register_blueprint(project, url_prefix='/api/projects')
    app.register_blueprint(cycles, url_prefix='/api/cycles')
    app.register_blueprint(test_cases, url_prefix='/api/cases')
