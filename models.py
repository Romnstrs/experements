from peewee import SqliteDatabase, Model, CharField, DateField, ForeignKeyField, BooleanField

db = SqliteDatabase('bot.sqlite3')

class User(Model):
    chat_id = CharField()

    class Meta:
        database = db

class Todo(Model):
    task = CharField()
    is_done = BooleanField()
    data = DateField()
    user = ForeignKeyField(User)

    class Meta:
        database = db

if __name__ == '__main__':
    db.create_tables([User, Todo])