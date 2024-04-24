import re
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = 'ADD_YOUR_BOT_TOKEN_HERE'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Give me a YouTube video URL & i will send the thumbnail.")



@bot.message_handler(func=lambda message: True)
def select_quality(message):

    URLpattern = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([\w-]+)'
    YTurls = re.search(URLpattern, message.text)

    if YTurls:
        vidID = YTurls.group(4)
        # vidURL = YTurls.group(0)

        def gen_markup():
            markup = InlineKeyboardMarkup() 
            markup.add(InlineKeyboardButton(text=f"High ✅", callback_data=f"high#{vidID}"))
            markup.add(
                InlineKeyboardButton(text=f"Medium",callback_data=f"medium#{vidID}"),
                InlineKeyboardButton(text=f"Low", callback_data=f"low#{vidID}")
            )
            return markup
        
        bot.reply_to(message=message, text="Choose a size:", reply_markup=gen_markup())     
    else:
        bot.reply_to(message=message, text="Please send me a youtube link.")


@bot.callback_query_handler(func=lambda call: True)
def download_thumbnail(call):
    
    data = call.data.split("#")
    receivedData = data[0]
    vidID = data[1]
    chatID = call.message.chat.id

    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    
    highThumb = f"https://img.youtube.com/vi/{vidID}/maxresdefault.jpg"
    mediumThumb = f"https://img.youtube.com/vi/{vidID}/hqdefault.jpg"
    lowThumb = f"https://img.youtube.com/vi/{vidID}/mqdefault.jpg"

    try:
        match receivedData:
            case "high":
                bot.send_photo(chatID, highThumb)
            case "medium":
                bot.send_photo(chatID, mediumThumb)
            case "low":
                bot.send_photo(chatID, lowThumb)
    except Exception as e:
        bot.send_message(chatID, f"Error: {e}.")
        print("\n - Error:", e)


print("YTThumbDownloader bot running..")
bot.infinity_polling()
