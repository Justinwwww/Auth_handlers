class AnonymousUser(login.AnonymousUserMixin):
 id = 0
 admin = False
 name = 'Anonymous'
 user_db = None

 def key(self):
   return None

 def has_permission(self, permission):
   return False


login_manager.anonymous_user = AnonymousUser


class FlaskUser(AnonymousUser):
 def __init__(self, user_db):
   self.user_db = user_db
   self.id = user_db.key.id()
   self.name = user_db.name
   self.admin = user_db.admin

 def key(self):
   return self.user_db.key.urlsafe()

 def get_id(self):
   return self.user_db.key.urlsafe()

 def is_authenticated(self):
   return True

 def is_active(self):
   return self.user_db.active

 def is_anonymous(self):
   return False

 def has_permission(self, permission):
   return self.user_db.has_permission(permission)


@login_manager.user_loader
def load_user(key):
 user_db = ndb.Key(urlsafe=key).get()
 if user_db:
   return FlaskUser(user_db)
 return None


login_manager.init_app(app)