import telebot
import random
from env import TOKEN
import requests
import csv
from bs4 import BeautifulSoup as BS
bot = telebot.TeleBot(TOKEN)

newsss={}
lin=[]
about=[]
img={}
keyboard = telebot.types.ReplyKeyboardMarkup()
button1 = telebot.types.KeyboardButton('More')
button2= telebot.types.KeyboardButton('Quiet')
button3=telebot.types.KeyboardButton('Photo')
button4 = telebot.types.KeyboardButton('Description')
keyboard1 = telebot.types.ReplyKeyboardMarkup()


keyboard.add(button1)
keyboard1.add(button2,button3,button4)

def get_html(url):
    response = requests.get(url)
    return response.text

def get_soup(html):
    soup =BS(html,'lxml')
    return soup

def get_news(soup):
    news=soup.find_all('a',class_='ArticleItem--name')
    i=1
    for new in news:
        if i==21:
            break
        try:
            new=new.text
        except AttributeError:
            new=None
        lin.append(new.strip())
        newsss.update({str(i):new.strip()})
        i+=1


    refers=soup.find_all('a',class_="ArticleItem--name")
    k=1
    for refer in refers:
        if k==21:
            break
        about.append(refer.get('href')) 
        print(f'{k} ссылка:',refer.get('href'))
        k+=1
    jp=soup.find_all('div',class_='ArticleItem')
    y=1
    for j in jp:
        if y==21:
            break
        e=j.find('a').get('href')
        img.update({str(y):e})
        y+=1
    
        

def about_new(message,str):
    url=zipped.get(str)
    html =get_html(url)
    soup=get_soup(html)
    get_info(message,soup)
    
def get_info(message,soup):
    aboutt=soup.find_all('div',class_='BbCode')
    for abou in aboutt:
        try:
            abou=abou.text.strip()
        except AttributeError:
            abou='=='
        bot.send_message(message.chat.id,f'{abou}')


url='https://kaktus.media/?lable=8&date=2022-12-21&order=time'
html =get_html(url)
soup=get_soup(html)
get_news(soup)
zipped=dict(zip(lin,about))
zipp=dict(zip(lin,img))



@bot.message_handler(commands=['start','hi'])
def start_function(message):
    bot.send_message(message.chat.id ,f'привет {message.chat.first_name},я подготовил для тебя новости на сегодня.Нажми кнопку Discription,а после выберите индекс фотографии,если хотите узнать о ней больше :',reply_markup=keyboard)
    y=1
    for key,val in newsss.items():
        bot.send_message(message.chat.id ,f'{y} новость: {val}')
        y+=1
    bot.register_next_step_handler(message, start_game)
       
def start_game(message):
    if message.text=='More':
        bot.send_message(message.chat.id,f'выберите что хотите узнать: ',reply_markup=keyboard1)
        bot.register_next_step_handler(message, more)

    else:
        bot.send_message(message.chat.id,'bye')
        
def more(message):
    if message.text=='Quiet':
        bot.send_message(message.chat.id,'Пока:')
        bot.send_sticker(message.chat.id,'CAACAgQAAxkBAAJJ62OhPUdMdg9xAAG0fETiq5E52VE3qgAC-REAAhUm0FAjCj4_qMDONywE')

    elif message.text=='Photo':
        w=bot.send_message(message.chat.id,'индекс фотографии: ')
        bot.register_next_step_handler(w, img_op)

    elif message.text=='Description':
        msg = bot.send_message(message.chat.id, 'Введи индекс :')
        bot.register_next_step_handler(msg,news_open)
        
def img_op(message):
    bot.send_photo(message.chat.id,img.get(str(message.text)))
    bot.send_message(message.chat.id,'Вернуться - More')
    bot.register_next_step_handler(message, start_game)

def news_open(message):
    bot.send_message(message.chat.id,f'====={newsss.get(str(message.text))}=====')
    about_new(message,newsss.get(str(message.text)))
    bot.send_message(message.chat.id,'Вернуться - More')
    bot.register_next_step_handler(message, start_game)
    
      
bot.polling()


