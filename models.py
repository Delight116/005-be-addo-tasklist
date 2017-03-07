import peewee as pw
from datetime import datetime as dt
import datetime

db = pw.SqliteDatabase('TaskList.db')


def initialize_database():
    User.create_table(fail_silently=True)
    Tasks.create_table(fail_silently=True)
    try:
        User.create(
            nikname='root',
            password='123',

        )
    except pw.IntegrityError:
        pass


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    nikname = pw.CharField(max_length=25, unique=True, null=False)
    firstname = pw.CharField(max_length=70, null=True)
    lastname = pw.CharField(max_length=70, null=True)
    password = pw.CharField(null=False)
    state = pw.BooleanField(default=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.state

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nikname)


class Tasks(BaseModel):
    user = pw.ForeignKeyField(User)
    task_title = pw.CharField(max_length=70, null=False)
    task_date = pw.TimestampField(default=dt.today())
    task_to_date = pw.TimestampField(default=dt.today()+datetime.timedelta(days=1))
    task_text = pw.CharField(max_length=256)
    task_status = pw.BooleanField(default=False)

    def is_active(self):
        return self.task_status

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<Tasks %r>' % (self.task_title)


