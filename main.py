import telebot
from telebot import types
import sqlite3

# توكن البوت
TOKEN = '7746175503:AAEiBiB8LfGxAkEoIE0wbjGyNx3CVCNSKfY'
bot = telebot.TeleBot(TOKEN)

# إعداد قاعدة البيانات
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0)")
conn.commit()

# تسجيل المستخدم عند /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO users (id, points) VALUES (?, ?)', (user_id, 0))
        conn.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('كسب نقاط', 'رصيدي', 'سحب النقاط')
    bot.send_message(user_id, 'أهلاً بك في بوت قحطاني لزيادة المتابعين!', reply_markup=markup)

# كسب نقاط
@bot.message_handler(func=lambda msg: msg.text == 'كسب نقاط')
def earn_points(message):
    user_id = message.chat.id
    cursor.execute('UPDATE users SET points = points + 50 WHERE id=?', (user_id,))
    conn.commit()
    bot.send_message(user_id, 'تمت إضافة 50 نقطة لحسابك!')

# رصيدي
@bot.message_handler(func=lambda msg: msg.text == 'رصيدي')
def check_points(message):
    user_id = message.chat.id
    cursor.execute('SELECT points FROM users WHERE id=?', (user_id,))
    points = cursor.fetchone()[0]
    bot.send_message(user_id, f'رصيدك الحالي هو: {points} نقطة.')

# سحب النقاط
@bot.message_handler(func=lambda msg: msg.text == 'سحب النقاط')
def withdraw_points(message):
    user_id = message.chat.id
    cursor.execute('SELECT points FROM users WHERE id=?', (user_id,))
    points = cursor.fetchone()[0]
    if points >= 100:
        cursor.execute('UPDATE users SET points = points - 100 WHERE id=?', (user_id,))
        conn.commit()
        bot.send_message(user_id, 'تم سحب 100 نقطة، سيتم إضافة 10 متابعين لحسابك قريباً.')
        # ربط مستقبلي مع API خارجي لطلب المتابعين
    else:
        bot.send_message(user_id, 'رصيدك لا يكفي، تحتاج 100 نقطة على الأقل.')

# تشغيل البوت
bot.infinity_polling()
