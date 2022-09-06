import telebot
from telebot import types
from scraper import get_clubs_from_search, club_info
import state


bot = telebot.TeleBot('5691964983:AAHEopCd7CtrXwY-_NlGkI_vg4ZdkQjqZCk')


@bot.message_handler(commands=['start'])
def start(message):
    msg = f"""Hello, <b>{message.from_user.first_name}</b> \n/help for commands list \n/search for search options"""

    bot.send_message(message.chat.id, msg, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    msg = f"""You can use the following commands: \n/search to search for a team or a player"""

    bot.send_message(message.chat.id, msg, parse_mode='html')

@bot.message_handler(commands=['search'])
def search(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    player_search = types.KeyboardButton("Search for a player")
    team_search = types.KeyboardButton("Search for a team")

    markup.add(player_search, team_search)

    bot.send_message(message.chat.id, 'Choose an option:', reply_markup=markup)


@bot.message_handler(func = lambda message: message.text in ['Search for a player','Search for a team'])
def team_search(message):
    if message.text == 'Search for a team':
        msg = bot.send_message(message.chat.id, "Type the name of the team", reply_markup=types.ForceReply(selective=False))
        bot.register_next_step_handler(msg, get_search_url)


def get_search_url(message):
    """Taking user request and forming a search url. then calling get_clubs_from_search """
    search_request = message.text.split()
    final_query = ""
    for i in range(len(search_request)):
        if i != (len(search_request)-1):
            final_query += f"{search_request[i]}+"
        else:
            final_query += f"{search_request[i]}"
    
    url = f"https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query={final_query}"

    data = get_clubs_from_search(url)

    bot.register_next_step_handler(message, return_search(message, data))
    


def return_search(message, data):
    """Presenting dataframe to user and asking to choose a team"""

    msg = "Please choose the team:\n\n"
    markup = types.ReplyKeyboardMarkup(True)

    for i in range(len(data)):
        msg += f"""{i+1}. {data.loc[i]['club_names']} from {data.loc[i]['country_names']}\n"""
        markup.add(types.KeyboardButton(i+1))

    
    bot.send_message(message.chat.id, msg, parse_mode='html', reply_markup=markup)
    




# @bot.message_handler(func = lambda message: message.text in ['1','2','3','4','5','6','7','8','9','10'])
# def send_to_club_page(message):
#     """Scraping from the page of the chosen team"""
    
#     index = int(message.text)-1
#     print(index)
#     # url = data.loc[index]['urls']
#     # club_data = club_info(url)
#     # departures = club_data[0]
#     # arrivals = club_data[1]
#     # mv = club_data[2]
#     # msg = "hello"
#     # departures_mess = "Top arrivals are:\n\n"
#     # for i in range(len(departures)):
#     #     departures_mess += f"""{departures.loc[i]['Players']}"""
#     # bot.send_message(message.chat.id, departures, parse_mode='html')

bot.polling(none_stop=True)