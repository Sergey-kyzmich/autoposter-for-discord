import discord
from discord import SelectOption
from discord.ui import View, Select, Button
from discord.ext import commands
import sys
import os
import datetime
from subprocess import Popen
import json
import asyncio
chanal_list = [1149439936378978457, 1149440272300789770, 1156213350947094598, 1167114128494698596, 1149440871889129573, 1149440945973116959, 1149441166094385254, 1149442358975402127,1149442451388506172, 1152705855205150742]


text_write = """
## Выбери то, что хочешь отредактировать:
**
## Пояснения по пункту "Запустить сейчас?":
1) Используется, если требуется запустить autoposter не ожидая кд с предыдущего сообщения.
2) КД - время, которое ждет autoposter с предыдущей отправки сообщения.(не путать с кд в discord канале)
3) 1-Да, запустить. В ином случае пропустить этот пункт.
4) Строго через запятую!!!
**
"""

#--------------------------------------Добавить ссылку на сообщение из канала новости
text_instruction = """

# Оплата подписки:
**
1) Пишем команду /buy
2) Выбираем желаемый период подписки.(нажимаем на нужную кнопку)
3) Оплачиваем подписку.
4) После покупки, вам будет выдан 16-ти значный код
5) Нажимаем на кнопку "Я оплатил" и вводим туда наш код
6) Если все удачно, то бот автоматически выдаст подписку и оповестит вас об этом. 
7) Рекомендуем записывать процесс оплаты на случай возникновения проблем.
**

# Получение токена:
**
1) Заходим в свой аккаунт на сайте discord.
2) Нажимаем ctrl+shift+i, переходим на вкладку Network.
3) В поиске пишем API, нажимаем ctrl+R.
4) В одной из появившихся вкладок находим Autorization, копируем искомый токен напротив.
5) Переходим обратно к боту, прописываем команду /menu.
6) Нажимаем на кнопку Токен и вставляем туда наш токен.**

# Редактирование данных:
**
1) Пишем команду /menu.
3) Выбираем желаемую категорию среди кнопок.
4) В 1-е окно пишется желаемое название категории.(Если название будет отличаться от стандартного(список стандартных названий тут:), то emoji не будет)
5) В 2-е окно вписываем id канала, в который будет отправляться сообщение.
6) В 3-е окно пишем текст нашего сообщения.
7) В 4-е окно вставляем ссылку на картинку.
8) В 5-е окно вставляем время между отправкой сообщений(в минутах), Запустить сейчас?.

## Пояснения по пункту "Запустить сейчас?":
1) Используется, если требуется запустить autoposter не ожидая кд с предыдущего сообщения.
2) КД - время, которое ждет autoposter с предыдущей отправки сообщения.(не путать с кд в discord канале)
3) 1-Да, запустить. В ином случае пропустить этот пункт.
4) Строго через запятую!!!

**
# Включение Autoposter:
**
1) Пишем команду /menu.
2) В выпадающем списке под кнопками выбираем нужные категории.
**
# Получение id канала:
**
1) Заходим в настройки discord.
2) Находим вкладку "Расширенные".
3) Включаем режим разработчика.
4) Нажимаем правой кнопкой мыши по интересующему нас каналу.
5) Внизу копируем id канала.**
"""

derictori = os.getcwd().replace("\\", "/")
intents = discord.Intents.all()

text_else_menu = """**Требуется приобрести подписку.**
**
Для покупки подписки - /buy
Меню с командами - /help**"""


text_change = "**Выберире authoposter, которые будут активны:**"

text_menu = """# Добро пожаловать в главное меню autoposter.
## Подробная инструкция: /insruction"""



config = {
    'token': ''
    'prefix': '/',
}

ids = 0

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
bot.remove_command('help')


def find_lable_name(k, data):
    label_name = ["Транспорт", "Недвижимость", "Бизнес", "Оказание Услуг", "Барахолка", "Одежда", "Custom",
                  "Черный Рынок"]
    label_emoji = ["🚗", "🏡", "💼", "📋", "🎒", "👔", "👉", "🔪"]
    try:
        a = ["", label_emoji[label_name.index(data[str(k)])]][int(*[data[str(k)] in label_name])]
        return a
    except ValueError:
        return ""

def replace_chanal(interaction):
    view = View()
    with open(derictori + "/baze/" + str(interaction.user.id) + "/on_list.json", "r") as f:
        on_listed = json.load(f)
    with open(derictori + "/baze/" + str(interaction.user.id) + "/name_button.json", "r") as read:
        data = json.load(read)
    options = []
    for i in range(1, 9):
        if find_lable_name(i, data) == "":
            options.append(SelectOption(label=data[str(i)], default=on_listed[str(i)]))
        else:
            options.append(SelectOption(label=data[str(i)], emoji=find_lable_name(i, data), default=on_listed[str(i)]))

    select = Select(
        min_values=0,
        max_values=8,
        placeholder="Выбери какие каналы запустить!",
        options=options[:6]+[options[7]]+[options[6]],#a[:6]+[a[7]]+[a[6]]
    )
    return select

def replace_chanal_calback(interaction, select):
    on_list = []
    with open(derictori+"/baze/"+str(interaction.user.id)+"/name_button.json", "r") as read:
        name = json.load(read)
    values = select.values
    if name["1"] in values:
        on_list.append(True)
    else:
        on_list.append(False)
    if name["2"] in values:
        on_list.append(True)
    else:
        on_list.append(False)
    if name["3"] in values:
        on_list.append(True)
    else:
        on_list.append(False)
    if name["4"] in values:
        on_list.append(True)
    else:
        on_list.append(False)
    if name["5"] in values:
        on_list.append(True)
    else:
        on_list.append(False)
    if name["6"] in values:
        on_list.append(True)
    else:
        on_list.append(False)
    if name["7"] in values:
        on_list.append(True)
    else:
        on_list.append(False)
    if name["8"] in values:
        on_list.append(True)
    else:
        on_list.append(False)
    data = {
        "1": on_list[0],
        "2": on_list[1],
        "3": on_list[2],
        "4": on_list[3],
        "5": on_list[4],
        "6": on_list[5],
        "7": on_list[6],
        "8": on_list[7]
    }
    with open(derictori + "/baze/" + str(interaction.user.id) + "/on_list.json", "w") as write_file:
        json.dump(data, write_file)
    # print("start")
    Popen([sys.executable, "baze/" + str(interaction.user.id) + "/" + "main.py"])

def before_by(id, next):
    global derictori
    if not os.path.isdir("baze/"+str(id)):
        os.mkdir("baze/"+str(id))
        with open("authoposter_text.txt", "r+") as g:
            text_authoposters = g.read()
        for i in range(1,9):
            with open(f"baze/{str(id)}/{i}.json", "w") as f:
                json.dump({"id_chanal": "", "text": "", "image": "", "time": "", "next_time": 0}, f)
            with open(f"baze/{str(id)}/{i}.py", "w") as f:
                f.write(f"id = {str(id)}\nk = {str(i)+str(text_authoposters).replace('п»ї', '')}")
        with open(f"baze/{str(id)}/token.txt", "w") as f:
            f.write("")
        data = {"1":False,"2":False,"3":False,"4":False,"5":False,"6":False,"7":False,"8":False,}
        with open(f"baze/{str(id)}/on_list.json", "w") as f:
            json.dump(data, f)
        with open(f"baze/{str(id)}/main.py", "w") as f:
            with open("main_text.txt", "r") as read_file:
                f.write(f"id = {id}{read_file.read()[1:].replace('п»ї', '')}")
        data_name_button = {'1': 'Транспорт', '2': 'Недвижимость', '3': 'Бизнес', '4': 'Оказание Услуг', '5': 'Барахолка', '6': 'Одежда', '7': 'Custom', '8': 'Черный Рынок'}
        with open(f"baze/{str(id)}/name_button.json", "w") as write_json:
            json.dump(data_name_button, write_json)
    with open(derictori + "/baze/" + str(id) + "/pay_to.txt", "w") as write_pay_to:
        write_pay_to.write(str(next))
# before_by(679385458731384832, "2100,1,1,1,1")
def for_class(self,derictori, k):
    with open("for_modal_file.txt", "r") as f:
        s = f.readline()
    with open(derictori + "/baze/" + s + "/" + str(k) + ".json", "r") as read_file:
        data = json.load(read_file)
    with open(derictori + "/baze/" + s + "/name_button.json", "r") as read_file:
        name_button = json.load(read_file)

    self.add_item(discord.ui.InputText(label="Название категории:",style=discord.InputTextStyle.short, value=name_button[str(k)], required=False))
    self.add_item(discord.ui.InputText(label="ID Канала:", value=data["id_chanal"], required=False))
    self.add_item(discord.ui.InputText(label="Текст сообщения:", style=discord.InputTextStyle.long, value=data["text"],required=False))
    self.add_item(discord.ui.InputText(label="Сылка на фото:", value=data["image"], required=False))
    self.add_item(discord.ui.InputText(label="Частота отправки сообщений, Запустить сейчас?", value=data["time"], required=False))

def callback_for_class(self, interaction: discord.Interaction,k):
    self_4 = self.children[4].value
    if [int(self_4.find(',')) != -1] != [False]:
        if ("1" in self_4[self_4.index(",")+1:] or "да" in self_4[self_4.index(",")+1:] or "Да" in self_4[self_4.index(",")+1:])\
            or "ДА" in self_4[self_4.index(",")+1:]or "lf" in self_4[self_4.index(",")+1:] or "LF" in self_4[self_4.index(",")+1:]:
            newself = "0"
        else:
            newself = "1"
    else:
        newself = "1"
    dt1 = datetime.datetime(2023, 12, 23, 0, 0, 0)
    dt2 = datetime.datetime.now()
    tdelta = dt2 - dt1
    data = {
        "id_chanal": self.children[1].value,
        "text": self.children[2].value,
        "image": self.children[3].value,
        "time": self.children[4].value.split(",")[0],
        "next_time": int(str(tdelta.total_seconds())[:str(tdelta.total_seconds()).index(".")]) * int(
            newself)}
    with open(derictori + "/baze/" + str(interaction.user.id) + "/"+str(k)+".json",
              "w") as write_file:  # тут
        json.dump(data, write_file)
    if newself == "0":
        with open(derictori + "/baze/" + str(interaction.user.id) + "/on_list.json", "r") as read_file:
            read = json.load(read_file)
        read[str(k)]=True
        with open(derictori + "/baze/" + str(interaction.user.id) + "/on_list.json", "w") as write_file:
            json.dump(read, write_file)
        Popen([sys.executable, "baze/" + str(interaction.user.id) + "/" + "main.py"])
    if self.children[0].value !="":
        with open(derictori + "/baze/" + str(interaction.user.id) + "/name_button.json", "r") as read_file:
            name_button = json.load(read_file)
        d=True
        # print(name_button)
        for w in name_button:
            if self.children[0].value == name_button[str(w)]:
                # print(self.children[0].value, name_button[str(w)])
                d = False

        if d==True:
            name_button[str(k)] = self.children[0].value
            with open(derictori + "/baze/" + str(interaction.user.id) + "/name_button.json", "w") as write_file:
                json.dump(name_button, write_file)

class transport(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for_class(self,derictori,1)

    async def callback(self, interaction: discord.Interaction):
        callback_for_class(self, interaction, 1)
        await interaction.response.send_message(content="## Данные изменены!")

class house(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for_class(self, derictori, 2)

    async def callback(self, interaction: discord.Interaction):
        callback_for_class(self, interaction, 2)
        await interaction.response.send_message(content="## Данные изменены!")

class biznes(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for_class(self, derictori, 3)

    async def callback(self, interaction: discord.Interaction):
        callback_for_class(self, interaction, 3)
        await interaction.response.send_message(content="## Данные изменены!")

class uslug(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for_class(self, derictori, 4)

    async def callback(self, interaction: discord.Interaction):
        callback_for_class(self, interaction, 4)
        await interaction.response.send_message(content="## Данные изменены!")

class baraholka(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for_class(self, derictori, 5)

    async def callback(self, interaction: discord.Interaction):
        callback_for_class(self, interaction, 5)
        await interaction.response.send_message(content="## Данные изменены!")

class men_odez(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for_class(self, derictori, 6)

    async def callback(self, interaction: discord.Interaction):
        callback_for_class(self, interaction, 6)
        await interaction.response.send_message(content="## Данные изменены!")

class custom(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for_class(self, derictori, 7)

    async def callback(self, interaction: discord.Interaction):
        callback_for_class(self, interaction, 7)
        await interaction.response.send_message(content="## Данные изменены!")

class black_market(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for_class(self, derictori, 8)

    async def callback(self, interaction: discord.Interaction):
        callback_for_class(self, interaction, 8)
        await interaction.response.send_message(content="## Данные изменены!")

class token(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        with open("for_modal_file.txt", "r") as f:
            s = f.readline()
        with open(derictori+"/baze/" + str(s) + "/token.txt", "r+") as f:
            token = f.read()
        self.add_item(discord.ui.InputText(label="Ваш токен:", value= token))

    async def callback(self, interaction: discord.Interaction):
        f = open(derictori+"/baze/" + str(interaction.user.id) + "/token.txt", "w")
        f.write(str(self.children[0].value))
        f.close
        await interaction.response.send_message(content="## Данные изменены!")


class activate_subscription(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="Ваш код активации:"))

    async def callback(self, interaction: discord.Interaction):
        with open(f"token_{str(self.children[0].value)[:2]}_day.txt") as read_token_7_day:
            if self.children[0].value in read_token_7_day.read():
                day=str(self.children[0].value)[:2]
            else:
                day=0
        if day==0:
            await interaction.response.send_message(content="## Токен не найден!")
        else:
            with open(f"token_{day}_day.txt", "r") as _open: # удаление токена активации
                read = _open.readlines()
                read = read[:read.index(self.children[0].value + "\n")] + read[read.index(self.children[0].value + "\n") + 1:]
                with open(f"token_{day}_day.txt", "w") as _close:
                    _close.writelines(read)
            with open('User_list.txt', 'r', encoding="utf-8") as file:# Проверка на наличие активной подписки
                read_str_list = file.read()
            if str(interaction.user.id) not in read_str_list:
                with open('User_list.txt', 'w', encoding="utf-8") as file:
                    file.write(read_str_list+"2023,12,23,0,0,0 "+str(interaction.user.id)+"\n")
            with open('User_list.txt', 'r', encoding="utf-8") as file:# Проверка на наличие активной подписки
                readlist = file.readlines()
            for g in range(len(readlist)):
                if str(interaction.user.id) in readlist[g]:
                    a = readlist[g]
                    break
            a = a[:a.index(" ")]
            d = a.split(",")
            dt1 = datetime.datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]))
            dt2 = datetime.datetime.now()
            tdelta = dt1 - dt2
            if day=="99":
                next = "2100,1,1,1,1"
                readlist[g] = next +" "+ str(interaction.user.id)
            else:
                if int(tdelta.total_seconds()) > 0:
                    next = tdelta + datetime.datetime.now() + datetime.timedelta(days=int(day))
                    readlist[g] = str(next).replace("-", ",").replace(":", ",").replace(" ", ",")[:-3] + " " + str(interaction.user.id)+"\n"
                else:
                    next = datetime.datetime.now() + datetime.timedelta(days=int(day))
                    readlist[g] = str(next).replace("-", ",").replace(":", ",").replace(" ", ",")[:-3] + " " + str(interaction.user.id)+"\n"

            with open('User_list.txt', 'w', encoding="utf-8") as file:
                file.writelines(readlist)
            before_by(interaction.user.id, str(next).replace("-", ",").replace(":", ",").replace(" ", ",")[:-3])

            await interaction.response.send_message(content="## Подписка активирована!")


@bot.slash_command(name="help", description = "Команда для отображения списка команд.")
async def _help(interaction):
    if interaction.channel.id not in chanal_list:
        with open("commands_list.txt", 'r', encoding="utf8") as f:
            ab = f"**\n{f.read()}**"
        await interaction.response.send_message(content=ab)
    else:
        await interaction.response.send_message(content="## В этом канале нельзя использовать данную команду!", ephemeral=True)


@bot.slash_command(name = "buy", description = "Команда для оплаты подписки.")
async def _buy(interaction):
    if interaction.channel.id not in chanal_list:
        view = View()
        button_buy_1 = Button(label = "Неделя", url = "https://www.digiseller.market/asp2/pay_wm.asp?id_d=4171083&lang=ru-RU", style= discord.ButtonStyle.green)
        button_buy_2 = Button(label = "Месяц", url = "https://www.digiseller.market/asp2/pay_wm.asp?id_d=4171091&lang=ru-RU", style= discord.ButtonStyle.green)
        button_buy_3 = Button(label = "Навсегда", url = "https://www.digiseller.market/asp2/pay_wm.asp?id_d=4171097&lang=ru-RU", style= discord.ButtonStyle.green)
        button_4 = Button(label="Я оплатил!")
        button_youtube = Button(label =  "Подробная инструкция!", url = "https://youtu.be/JmcvvGAgbng")# Сюда надо добавить ссылку на видео



        view.add_item(button_buy_1)
        view.add_item(button_buy_2)
        view.add_item(button_buy_3)
        view.add_item(button_4)
        view.add_item(button_youtube)


        async def button_4_calback(interaction):
            modal = activate_subscription(title="Активация Autoposter")
            await interaction.response.send_modal(modal=modal)

        button_4.callback = button_4_calback
        with open('prise.txt', 'r', encoding="utf-8") as file:
            text = file.read()
        await interaction.response.send_message(content=f"**{text}**", view=view)

    else:
        await interaction.response.send_message(content="## В этом канале нельзя использовать данную команду!", ephemeral=True)


@bot.slash_command(name="menu", description = "Основное меню authoposter")
async def _menu(interaction):

    if interaction.channel.id not in chanal_list:
        with open('User_list.txt', 'r', encoding="utf-8") as file:
            read = file.read()
        if str(interaction.user.id) not in read:#Проверка на наличие
            await interaction.response.send_message(content=text_else_menu)

        else:

            with open('User_list.txt', 'r', encoding="utf-8") as file:
                readlist = file.readlines()
            f=False
            for g in range(len(readlist)):
                if str(interaction.user.id) in readlist[g]:
                    a = readlist[g]
                    f = True
                    break
            a = a[:a.index(" ")]
            d = a.split(",")
            dt1 = datetime.datetime(int(d[0]), int(d[1]), int(d[2]), int(d[3]), int(d[4]))
            dt2 = datetime.datetime.now()
            tdelta = dt1 - dt2

            if int(tdelta.total_seconds())>0:
                if int(d[0])==2100: days = "\n ## До конца подписки осталось: ထ"
                else:days = f"\n ## До конца подписки осталось Дней: {tdelta.days}, Часов: {int(tdelta.total_seconds()) // 3600 - tdelta.days * 24}, Минут: {(int(tdelta.total_seconds()) % 3600) // 60}"


                with open(derictori+"/baze/"+str(interaction.user.id)+"/name_button.json", "r") as  read:
                    data = json.load(read)
                button = []
                for i in range(1, 9):
                    if find_lable_name(i, data)=="":
                        button.append(Button(label=data[str(i)], style=discord.ButtonStyle.primary))
                    else:
                        button.append(Button(label=data[str(i)], emoji=find_lable_name(i, data),style=discord.ButtonStyle.primary))

                button_9 = Button(label="Токен", emoji="🔑", style=discord.ButtonStyle.primary)
                select = replace_chanal(interaction)
                #(•_•) ( •_•)>⌐■-■ (⌐■_■)
                view = View()

                view.add_item(button[0])
                view.add_item(button[1])
                view.add_item(button[2])
                view.add_item(button[3])
                view.add_item(button[4])
                view.add_item(button[5])
                view.add_item(button[7])
                view.add_item(button[6])
                view.add_item(button_9)
                view.add_item(select)



                async def button_1_callback(interaction: discord.Interaction):
                    with open("for_modal_file.txt", "w") as f:
                        f.write(str(interaction.user.id))
                    modal = transport(title=name["1"])
                    await interaction.response.send_modal(modal=modal)

                async def button_2_callback(interaction: discord.Interaction):
                    with open("for_modal_file.txt", "w") as f:
                        f.write(str(interaction.user.id))
                    modal = house(title=name["2"])
                    await interaction.response.send_modal(modal=modal)

                async def button_3_callback(interaction: discord.Interaction):
                    with open("for_modal_file.txt", "w") as f:
                        f.write(str(interaction.user.id))
                    modal = biznes(title=name["3"])
                    await interaction.response.send_modal(modal=modal)

                async def button_4_callback(interaction: discord.Interaction):
                    with open("for_modal_file.txt", "w") as f:
                        f.write(str(interaction.user.id))
                    modal = uslug(title=name["4"])
                    await interaction.response.send_modal(modal=modal)

                async def button_5_callback(interaction: discord.Interaction):
                    with open("for_modal_file.txt", "w") as f:
                        f.write(str(interaction.user.id))
                    modal = baraholka(title=name["5"])
                    await interaction.response.send_modal(modal=modal)

                async def button_6_callback(interaction: discord.Interaction):
                    with open("for_modal_file.txt", "w") as f:
                        f.write(str(interaction.user.id))
                    modal = men_odez(title=name["6"])
                    await interaction.response.send_modal(modal=modal)

                async def button_7_callback(interaction: discord.Interaction):
                    with open("for_modal_file.txt", "w") as f:
                        f.write(str(interaction.user.id))
                    modal = custom(title=name["7"])
                    await interaction.response.send_modal(modal=modal)

                async def button_8_callback(interaction: discord.Interaction):
                    with open("for_modal_file.txt", "w") as f:
                        f.write(str(interaction.user.id))
                    modal = black_market(title=name["8"])
                    await interaction.response.send_modal(modal=modal)

                async def button_9_callback(interaction: discord.Interaction):
                    with open("for_modal_file.txt", "w") as f:
                        f.write(str(interaction.user.id))
                    modal = token(title="Токен")
                    await interaction.response.send_modal(modal=modal)
                async def select_calback(interaction: discord.Interaction):
                    replace_chanal_calback(interaction, select)
                    await interaction.response.send_message(content="## Активные каналы отредактированы!")

                with open(derictori + f"/baze/{interaction.user.id}/name_button.json", "r") as json_load:
                    name = json.load(json_load)
                button_9.callback = button_9_callback
                button[7].callback = button_8_callback
                button[6].callback = button_7_callback
                button[5].callback = button_6_callback
                button[4].callback = button_5_callback
                button[3].callback = button_4_callback
                button[2].callback = button_3_callback
                button[1].callback = button_2_callback
                button[0].callback = button_1_callback
                select.callback = select_calback
                await interaction.response.edit_message(content=text_write, view=view,)
                # button_change.callback = change_callback
                # button_on.callback = button_on_calback
                await interaction.response.send_message(content=text_menu+days, view= view)#+days --------------------------Кол-во дней до конца подписки
            else:
                await interaction.response.send_message(content=text_else_menu)



    else:
        await interaction.response.send_message(content="## В этом канале нельзя использовать данную команду!", ephemeral=True)


@bot.slash_command(name="instruction", description ="Инструкция по использованию authoposter")
async def _instruction(interaction):
    if interaction.channel.id not in chanal_list:
        button_1 = Button(label="Видео на youtube:", url = "https://youtu.be/JmcvvGAgbng")#https://www.youtube.com/channel/UClkJyVX90IXgVhHj4-9b-Qg")
        view = View()
        view.add_item(button_1)
        await interaction.response.send_message(content=text_instruction, view = view)
    else:
        await interaction.response.send_message(content="## В этом канале нельзя использовать данную команду!", ephemeral=True)

@bot.event
async def on_ready():
    root = derictori+"/baze"
    print("start bot")
    list = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
    for i in list:
        Popen([sys.executable, "baze/" + str(i) + "/" + "main.py"])
    # print(f"{list=}")


try:
    bot.run(config["token"])
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("python restarter.py")
    os.system('kill 1')

