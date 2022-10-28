import telebot
import models
from datetime import date
import schedule
import time
from threading import Thread

bot = telebot.TeleBot('5327317275:AAEqLFXfk8l4E3BvrNT0JFkZp3yOGAfk7hU')


@bot.message_handler(commands=["start"])
def start_handler(message):
    if not models.User.select().where(models.User.chat_id == message.chat.id):
        models.User.create(chat_id = message.chat.id)
    bot.send_message(
        message.chat.id,
        f"Hello {message.chat.first_name} {message.chat.last_name or ''}!")

def create_all_todo_message(chat_id):
    user = models.User.get(models.User.chat_id == chat_id)
    todos = models.Todo.select().where(models.Todo.user == user,
                                       models.Todo.data == date.today())
    message_text = ['']
    for todo in todos:
        if todo.is_done:
            message_text.append(f"<b><s>{todo.id}. {todo.task}</s></b>\n")
        else:
            message_text.append(f"<b>{todo.id}. {todo.task}</b>\n")
    return "".join(message_text)

@bot.message_handler(commands=['today','t'])
def get_todo_list(message):

    bot.send_message(
        message.chat.id,
        create_all_todo_message(message.chat.id),
        parse_mode='HTML'
    )

@bot.message_handler(regexp="\d+ done")
def make_done(message):
    todo_id = message.text.split(" ")[0]
    todo = models.Todo.get(models.Todo.id == todo_id)
    todo.is_done = True
    todo.save()
    bot.send_message(
        message.chat.id,
        f"{todo.task} is done now"
    )



@bot.message_handler(content_types=['text'])
def create_to_do_handler(message):
    user = models.User.get(models.User.chat_id == message.chat.id)
    models.Todo.create(
        task=message.text,
        is_done=False,
        user=user,
        data=date.today()
    )
    bot.send_message(
        message.chat.id, "Your todo was saved!"
    )

def check_notify():
    for user in models.User.select():
        todos = models.Todo.select().where(models.Todo.user == user,
                                           models.Todo.data == date.today(),
                                           models.Todo.is_done == False
                                           )
        if todos:
            bot.send_message(
                user.chat_id,
                create_all_todo_message(user.chat_id),
                parse_mode="HTML"
            )

def run_scheduler():
    schedule.every(10).seconds.do(check_notify)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=run_scheduler).start()
    bot.infinity_polling()

