from datetime import datetime
from app import app, db
from app.core.models import User, Role, Microapp


def create_users():
    """ Create users when app starts """
    from app.core.models import User, Role

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    user = find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    user = find_or_create_user(u'User', u'Example', u'user@example.com', 'Password1')

    # Add microapp
    microapp = find_or_create_microapp('app1', u'App1', False)
    microapp = find_or_create_microapp('app2', u'App2', False)

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user

def find_or_create_microapp(name, label, is_active):
    """ Find existing microapp or create new microapp """
    microapp = Microapp.query.filter(Microapp.name == name).first()
    if not microapp:
        microapp = Microapp(name=name, label=label, is_active=is_active)
        db.session.add(microapp)
    return microapp
