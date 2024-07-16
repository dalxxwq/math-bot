import telebot
import pickle
from telebot import types
from made_pictures import create_equation
from database import API_TOKEN, equation

bot = telebot.TeleBot(API_TOKEN)


# Відправляє вітання К при команді start або help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    username = message.from_user.first_name
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_test = types.KeyboardButton("Пройти тест🧮")
    btn_stop = types.KeyboardButton("Завершити🛑")
    keyboard.add(btn_test, btn_stop)
    bot.send_message(message.chat.id,
                     f"Привіт {username}, я створенний для того щоб допомагати вивчати вам математику. Я буду давати приклади і рівняння, а вам треба просто писати відповіді на них. "
                     f"Давай одразу перейдемо до тесту. У тебе є 10 рівнянь, чим більше ти пройдеш, тим більше ти зможеш. Удачі!",
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, test_choice)


# Вибір рівня
@bot.message_handler(func=lambda message: message.text == "Пройти тест🧮")
def test_choice(message):
    global is_test_active
    is_test_active = True  # Позначити тест як активний
    bot.send_message(message.chat.id, "Якщо ти хочеш пройти мій тест, ось список всіх рівнів:")
    keyboard = types.InlineKeyboardMarkup()

    for level in range(1):
        btn_level = types.InlineKeyboardButton(f"{level}️⃣ рівень", callback_data=f'level{level}')
        keyboard.add(btn_level)

    bot.send_message(message.chat.id, "Виберіть рівень:", reply_markup=keyboard)


# При необхідності є кнопка стоп
@bot.message_handler(func=lambda message: message.text == "Завершити🛑")
def stop_test(message):
    global is_test_active
    is_test_active = False  # Позначити тест як неактивний
    bot.send_message(message.chat.id, "Тест завершено. Дякую за участь!")


# Відповідає за вибір К
@bot.callback_query_handler(func=lambda call: call.data.startswith('level'))
def handle_level_selection(call):
    global is_test_active, current_level
    if is_test_active:
        level = int(call.data.replace('level', ''))
        current_level = level
        bot.send_message(call.message.chat.id, text=f"Ви вибрали {level} рівень!")
        test(call, level)
    else:
        bot.send_message(call.message.chat.id,
                         "Тест завершено або ще не розпочато. Натисніть 'Пройти тест🧮' щоб розпочати новий тест.")


# Сам тест
def test(call, level):
    global number_of_equation, equations_correct_count
    number_of_equation = 0
    equations_correct_count = 0  # Скидати лічильник правильних відповідей
    send_equation(call.message, level)


# Відповідає за надсилання прикладів
def send_equation(message, level):
    global number_of_equation, is_test_active, equations_correct_count
    if not is_test_active:
        return
    if number_of_equation < 50:
        bot.send_message(message.chat.id, text="Ось твій приклад")
        create_equation(number_of_equation)
        with open("Equation/new_img.png", "rb") as file:
            bot.send_photo(message.chat.id, file)
        bot.register_next_step_handler(message, check_answer, level)
    else:
        bot.send_message(message.chat.id, f"Вітаю! Ти вже пройшов всі 10 рівнянь у рівні {level}.")
        update_progress()


# Перевіряє відповідь
def check_answer(message, level):
    global number_of_equation, is_test_active, equations_correct_count
    if not is_test_active:
        return
    answer = message.text
    if answer == list(equation.values())[number_of_equation]:
        equations_correct_count += 1
        number_of_equation += 1
        bot.send_message(message.chat.id, "Молодець! Правильна відповідь.")
        if equations_correct_count == 10:
            bot.send_message(message.chat.id, f"Вітаю! Ти пройшов всі 10 рівнянь у рівні {level}.")
            update_progress()
        else:
            send_equation(message, level)
    else:
        bot.send_message(message.chat.id, "Нажаль це неправильна відповідь. Спробуй ще раз.")

        send_equation(message, level)


# Зберігає прогресс
def update_progress():
    global correct_level
    correct_level += 1
    with open("data_of_progress.txt", "wb") as save:
        pickle.dump(correct_level, save)


bot.polling()
