# ***************************************
# APPS VERZION
VERSION = [1, 2, 11, 'beta', 2023]
# ***************************************

# n, ne, e, se, s, sw, w, nw,
# -------------------------------
# |  -  |  -  |   n    |  -  |  -  |
# |:---:|:---:|:------:|:---:|:---:|
# |  -  | nw  |   -    | ne  |  -  |
# |  w  |  -  | center |  -  |  e  |
# |  -  | sw  |   -    | se  |  -  |
# |  -  |  -  |   s    |  -  |  -  |

# ***************************************
# IMPORT MODUL

import tkinter as tk
import os
import pytz
import sys
import psutil
import platform
import GPUtil
import subprocess as sp
import json
import requests
import qbittorrentapi
import subprocess
import zipfile

from tqdm import tqdm
from tabulate import tabulate
from bs4 import BeautifulSoup as bs
from tkinter import *
from tkinter import messagebox
from tkinter import Tk, Button
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

# ***************************************

# ***************************************
my_windows = tk.Tk()
my_windows.title('WindowsGuiPY')
my_windows.geometry('800x400')
my_windows.resizable(False, False)
my_menubar = tk.Menu(my_windows)

ROOT_DIR = os.path.abspath(os.curdir)
response = open('config.json', encoding='utf-8')
data_jsonq = json.loads(response.read())
lang = (data_jsonq['config_language'][0])

path = ROOT_DIR + '/Language/' + lang + '.json'
isFile = os.path.isfile(path)

# ***************************************
# LANGUAGE FILE
if isFile:
    ROOT_DIR = os.path.abspath(os.curdir)
    language = ROOT_DIR + '/Language/' + lang + '.json'
    response = open(language, encoding='utf-8')
    data_lang_json = json.loads(response.read())

    # ***************************************
    # SCRIPT FILE
    def find_process(name):
        for proc in psutil.process_iter():
            try:
                if name.lower() in proc.name().lower():
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return None


    process1 = find_process("qbittorrent")
    process2 = find_process("plex media server")
    '''process3 = find_process("microsoft edge")'''

    my_dropdown_menu_favo = tk.Menu(my_menubar, tearoff=0)

    if process1 is not None:
        def qBittorent():
            host = data_jsonq['__COMMENT_QBITTORENT_WEBAPI__']['host'][0]
            port = data_jsonq['__COMMENT_QBITTORENT_WEBAPI__']['port'][0]
            username = data_jsonq['__COMMENT_QBITTORENT_WEBAPI__']['username'][0]
            password = data_jsonq['__COMMENT_QBITTORENT_WEBAPI__']['password'][0]

            qbt_client = qbittorrentapi.Client(
                host=host,
                port=port,
                username=username,
                password=password
            )

            try:
                qbt_client.auth_log_in()
            except qbittorrentapi.LoginFailed as e:
                print(e)

            from prettytable import PrettyTable
            table = PrettyTable()
            table.field_names = ['Web API', 'Verzio']
            table.max_width = 70
            xx = "qBittorrent"
            xxx = f'{qbt_client.app.version}'
            yy = "qBittorrent Web API"
            yyy = f'{qbt_client.app.web_api_version}'
            table.add_row([xx, xxx])
            table.add_row([yy, yyy])

            for k, v in qbt_client.app.build_info.items():
                Web_API = f'{k}'
                Verzio = f'{v}'

                table.add_row([Web_API, Verzio])

            table1 = PrettyTable()
            table1.field_names = ['hash', 'name', 'state']
            table1.max_width = 200

            for torrent in qbt_client.torrents_info():
                hashh = f'{torrent.hash[-6:]}'
                name = f'{torrent.name}'
                state = f'{torrent.state}'
                table1.add_row([hashh, name, state])

            window = tk.Tk()
            window.title("qBittorrent API Info")
            window.geometry("300x300")
            window.resizable(False, False)

            scrollbar = tk.Scrollbar(window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text = tk.Text(window, yscrollcommand=scrollbar.set, wrap=tk.WORD, width=300, height=300)
            text.pack(side=tk.LEFT, fill=tk.BOTH)
            scrollbar.config(command=text.yview)

            text.insert(tk.END, str(table) + "\n")

            window = tk.Tk()
            window.title("qBittorrent API")
            window.geometry("900x400")
            window.resizable(False, False)

            scrollbar = tk.Scrollbar(window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text = tk.Text(window, yscrollcommand=scrollbar.set, wrap=tk.WORD, width=800, height=400)
            text.pack(side=tk.LEFT, fill=tk.BOTH)
            scrollbar.config(command=text.yview)

            text.insert(tk.END, str(table1))


        print(f"A qbittorrent program fut: pid={process1.pid}")
        my_dropdown_menu_favo.add_command(label=data_lang_json[lang][0]['MyFavUtils']['qBittorent'], command=qBittorent)
    else:
        print("A qbittorrent program nem fut.")

    if process2 is not None:
        def Plex_Media_server():
            ip = data_jsonq['__COMMENT_PLEX_SERVER_WEBAPI__']['ip']
            __aa__ = data_jsonq['__COMMENT_PLEX_SERVER_WEBAPI__']['__aa__']
            ports = data_jsonq['__COMMENT_PLEX_SERVER_WEBAPI__']['port']
            sections = data_jsonq['__COMMENT_PLEX_SERVER_WEBAPI__']['sections']
            Token = data_jsonq['__COMMENT_PLEX_SERVER_WEBAPI__']['X-Plex-Token']

            url = 'http://' + ip + __aa__ + ports + '/library/sections/' + sections + '/all?X-Plex-Token=' + Token
            responsee = requests.get(url)

            import xml.etree.ElementTree as ET

            root = ET.fromstring(responsee.text)

            from prettytable import PrettyTable

            table = PrettyTable()
            table.field_names = ['Title', 'Summary']
            table.max_width = 45

            for video in root.findall('./Video'):
                title = video.get('title') + '\n' + '-------------------------------------------->'
                summary = video.get('summary') + '\n' + '---------------------------------------------'
                table.add_row([title, summary])

            window = tk.Tk()
            window.title("Plex Media Server")
            window.geometry("800x400")
            window.resizable(False, False)

            # create a scrollbar
            scrollbar = tk.Scrollbar(window)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # create a text widget to display the table
            text = tk.Text(window, yscrollcommand=scrollbar.set, wrap=tk.WORD, width=800, height=400)
            text.pack(side=tk.LEFT, fill=tk.BOTH)
            scrollbar.config(command=text.yview)

            # insert the table into the text widget
            text.insert(tk.END, str(table))


        print(f"A plex media server program fut: pid={process2.pid}")
        my_dropdown_menu_favo.add_command(label=data_lang_json[lang][0]['MyFavUtils']['Plex_Media_server'],
                                          command=Plex_Media_server)
    else:
        print("A plex media server program nem fut.")

    '''if process3 is not None:
        print(f"A microsoft edge program fut: pid={process3.pid}")
    else:
        print("A microsoft edge program nem fut.")'''

    my_menubar.add_cascade(label=data_lang_json[lang][0]['MyFavUtils']['My_Favorite_Utilities'],
                           menu=my_dropdown_menu_favo)

    image = tk.PhotoImage(file=ROOT_DIR + "\\Script\\gui.png")
    canvas = tk.Canvas(my_windows, width=800, height=400)
    canvas.create_image(0, 0, image=image, anchor="nw")

    text_time = canvas.create_text(400, 180, text=" ", font=("Helvetica", 30, 'bold'), anchor="center")
    canvas.itemconfig(text_time, text=" ", fill="green2")
    text_date = canvas.create_text(400, 210, text=" ", font=("Helvetica", 20, 'bold'), anchor="center")
    canvas.itemconfig(text_date, text=" ", fill="green4")

    text_zipball_url = canvas.create_text(400, 395, text=" ", font=("Ethnocentric", 10, 'bold'), anchor="s")
    canvas.itemconfig(text_zipball_url, text=" ", fill="green4")
    text_published_at = canvas.create_text(795, 395, text=" ", font=("Ethnocentric", 10, 'bold'), anchor="se")
    canvas.itemconfig(text_published_at, text=" ", fill="green2")
    text_name = canvas.create_text(5, 395, text=" ", font=("Ethnocentric", 10, 'bold'), anchor="sw")
    canvas.itemconfig(text_name, text=" ", fill="green2")

    canvas.pack()

    # ****************************************
    # SCRIPT VIRUS SCAN
    class microsoft_apps:
        @staticmethod
        def virus_scann():
            parent_widget = Tk()
            parent_widget.title(data_lang_json[lang][0]['Microsoft']['Microsoft_Apps'])
            parent_widget.minsize(400, 150)
            parent_widget.geometry('400x150')

            pathh = 'C:\\Users\\leksz\\AppData\\Local\\Temp\\MpCmdRun.log'
            isFiles = os.path.isfile(pathh)

            def quick_scean():
                os.system(
                    'cmd.exe /k '
                    '"c: && '
                    'cd C:\\ProgramData\\Microsoft\\Windows Defender\\Platform\\4.18* && '
                    'start MpCmdRun -Scan -ScanType 1 && exit"')

            def full_scean():
                os.system(
                    'cmd.exe /k '
                    '"c: && '
                    'cd C:\\ProgramData\\Microsoft\\Windows Defender\\Platform\\4.18* && '
                    'start MpCmdRun -Scan -ScanType 2 && exit"')

            def open_log():
                if isFiles:
                    programName = "notepad.exe"
                    fileName = pathh
                    sp.Popen([programName, fileName])
                else:
                    messagebox.showinfo(data_lang_json[lang][0]['Messages']['Messages'],
                                        data_lang_json[lang][0]['Messages']['Messages_info_log'])

            def reset_log():

                if isFiles:
                    os.remove(pathh)
                else:
                    pass

            labelframe_widget = LabelFrame(parent_widget,
                                           text=data_lang_json[lang][0]['Microsoft']['Microsoft_security'])
            label_widget0 = Button(labelframe_widget, text=data_lang_json[lang][0]['Microsoft']['Sec_Quick'],
                                   command=quick_scean)
            label_widget1 = Button(labelframe_widget, text=data_lang_json[lang][0]['Microsoft']['Sec_Full'],
                                   command=full_scean)
            label_widget2 = Button(labelframe_widget, text=data_lang_json[lang][0]['Microsoft']['Sec_log_open'],
                                   command=open_log)
            label_widget3 = Button(labelframe_widget, text=data_lang_json[lang][0]['Microsoft']['Sec_log_reset'],
                                   command=reset_log)

            labelframe_widget.place(x=10, y=10, anchor='nw')
            label_widget0.pack()
            label_widget1.pack()
            label_widget2.pack()
            label_widget3.pack()


    def configure():
        programName = "notepad.exe"
        fileName = ROOT_DIR + "/config.json"
        sp.Popen([programName, fileName])


    def clock():
        # Aktuális idő lekérdezése
        dd = (''.join(data_jsonq['timezone'][0]))
        # current_time = time.strftime("%Y-%m-%d %H:%M:%S/%p")
        current_time = datetime.now(pytz.timezone(dd)).strftime("%H:%M:%S")
        current_date = datetime.now(pytz.timezone(dd)).strftime("%d-%m-%Y")

        canvas.itemconfig(text_time, text=current_time)
        canvas.itemconfig(text_date, text=current_date)
        my_windows.after(1000, clock)


    def verzions():
        url = requests.get("https://api.github.com/repos/LexyGuru/MyApps/releases")
        text = url.text
        data = json.loads(text)
        datas = data[0]

        __VERCH__ = "{a0}.{a1}.{a2}-{a3}-{a4}".format(
            a0=VERSION[0],
            a1=VERSION[1],
            a2=VERSION[2],
            a3=VERSION[3],
            a4=VERSION[4]
        )

        if __VERCH__ == datas['name']:
            zipball_url = datas['zipball_url']
            canvas.itemconfig(text_zipball_url, text=zipball_url)
            published_at = datas['published_at']
            canvas.itemconfig(text_published_at, text=published_at)
            name = datas['name']
            canvas.itemconfig(text_name, text=name)

        if __VERCH__ < datas['name']:
            menu_label_0 = tk.Label(my_windows, text=datas['zipball_url'], font=('Ethnocentric', 8), foreground='red')
            menu_label_1 = tk.Label(my_windows, text=datas['published_at'], font=('Ethnocentric', 8, 'bold'),
                                    foreground='red')
            menu_label_2 = tk.Label(my_windows, text=datas['name'], font=('Ethnocentric', 8, 'bold'), foreground='red')

            menu_label_0.place(relx=0.5, rely=1.0, anchor='s')
            menu_label_1.place(relx=1, rely=1, anchor='se')
            menu_label_2.place(relx=0.0, rely=1.0, anchor='sw')

            uppdate = tk.Label(my_windows, text="NEW UPDATE", font=('Ethnocentric', 25, 'bold'), foreground='red')
            uppdate.place(relx=0.5, rely=0.54, anchor='center')

        if __VERCH__ > datas['name']:
            ERROR = tk.Label(my_windows, text="UPDATE ERROR", font=('Ethnocentric', 25, 'bold'), foreground='red')
            ERROR.place(relx=0.5, rely=0.54, anchor='center')


    def weather_google():
        parent_widget = Tk()
        parent_widget.title('Weather Google')
        parent_widget.minsize(450, 750)
        parent_widget.geometry('450x750')

        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
                     "AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/94.0.4606.81 Safari/537.36"
        # US english
        LANGUAGE = data_jsonq['language_weather'][0]
        locat = data_jsonq['locations'][0]

        def get_weather_data(url):
            session = requests.Session()
            session.headers['User-Agent'] = USER_AGENT
            session.headers['Accept-Language'] = LANGUAGE
            session.headers['Content-Language'] = LANGUAGE
            html = session.get(url)
            # create a new soup
            soup = bs(html.text, "html.parser")

            # store all results on this dictionary
            result = {'region': soup.find("div", attrs={"id": "wob_loc"}).text,
                      'temp_now': soup.find("span", attrs={"id": "wob_tm"}).text,
                      'dayhour': soup.find("div", attrs={"id": "wob_dts"}).text,
                      'weather_now': soup.find("span", attrs={"id": "wob_dc"}).text,
                      'precipitation': soup.find("span", attrs={"id": "wob_pp"}).text,
                      'humidity': soup.find("span", attrs={"id": "wob_hm"}).text,
                      'wind': soup.find("span", attrs={"id": "wob_ws"}).text}

            next_days = []
            days = soup.find("div", attrs={"id": "wob_dp"})
            for day in days.findAll("div", attrs={"class": "wob_df"}):
                day_name = day.findAll("div")[0].attrs['aria-label']
                weather = day.find("img").attrs["alt"]
                temp = day.findAll("span", {"class": "wob_t"})
                max_temp = temp[0].text
                min_temp = temp[2].text
                next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})

            result['next_days'] = next_days
            return result

        URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather+" + locat
        import argparse

        parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
        parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                                    Default is your current location determined by your IP Address""",
                            default="")

        args = parser.parse_args()
        region = args.region
        if region:
            region = region.replace(" ", "+")
            URL += f"+{region}"

        data = get_weather_data(URL)

        labelframe_widget00 = LabelFrame(parent_widget, text=data_lang_json[lang][0]['Weather']['Weather'],
                                         font=('Ethnocentric', 10, 'bold'), foreground='green')

        label_widget_top0 = Label(labelframe_widget00,
                                  text=data_lang_json[lang][0]['Weather']['Weather_for'] + " " +
                                       data["region"], font=('Ethnocentric', 8, 'bold'))
        label_widget_top1 = Label(labelframe_widget00,
                                  text=data_lang_json[lang][0]['Weather']['Now'] + " " +
                                       data["dayhour"], font=('Ethnocentric', 8, 'bold'))
        label_widget_top2 = Label(labelframe_widget00,
                                  text=data_lang_json[lang][0]['Weather']['Temperature_now'] + " " +
                                       f"{data['temp_now']}°C", font=('Ethnocentric', 8, 'bold'))
        label_widget_top3 = Label(labelframe_widget00,
                                  text=data_lang_json[lang][0]['Weather']['Description'] + " " +
                                       data['weather_now'], font=('Ethnocentric', 8, 'bold'))
        label_widget_top4 = Label(labelframe_widget00,
                                  text=data_lang_json[lang][0]['Weather']['Precipitation'] + " " +
                                       data["precipitation"], font=('Ethnocentric', 8, 'bold'))
        label_widget_top5 = Label(labelframe_widget00,
                                  text=data_lang_json[lang][0]['Weather']['Humidity'] + " " +
                                       data["humidity"], font=('Ethnocentric', 8, 'bold'))
        label_widget_top6 = Label(labelframe_widget00,
                                  text=data_lang_json[lang][0]['Weather']['Wind'] + " " +
                                       data["wind"], font=('Ethnocentric', 8, 'bold'))

        labelframe_widget00.place(x=300, y=10, anchor='n')
        label_widget_top0.pack()
        label_widget_top1.pack()
        label_widget_top2.pack()
        label_widget_top3.pack()
        label_widget_top4.pack()
        label_widget_top5.pack()
        label_widget_top6.pack()

        for _ in data["next_days"]:
            pass

        labelframe_widget = LabelFrame(parent_widget, text=data["next_days"][0]['name'],
                                       font=('Ethnocentric', 10, 'bold'), foreground='green')
        label_widget0 = Label(labelframe_widget,
                              text=data_lang_json[lang][0]['Weather']['Description'] + " " + data["next_days"][0][
                                  'weather'])
        label_widget1 = Label(labelframe_widget,
                              text=data_lang_json[lang][0]['Weather']['Max_temperature'] + " " + data["next_days"][0][
                                  'max_temp'])
        label_widget2 = Label(labelframe_widget,
                              text=data_lang_json[lang][0]['Weather']['Min_temperature'] + " " + data["next_days"][0][
                                  'min_temp'])

        labelframe_widget1 = LabelFrame(parent_widget, text=data["next_days"][1]['name'],
                                        font=('Ethnocentric', 10, 'bold'), foreground='green')
        label_widget3 = Label(labelframe_widget1,
                              text=data_lang_json[lang][0]['Weather']['Description'] + " " + data["next_days"][1][
                                  'weather'])
        label_widget4 = Label(labelframe_widget1,
                              text=data_lang_json[lang][0]['Weather']['Max_temperature'] + " " + data["next_days"][1][
                                  'max_temp'])
        label_widget5 = Label(labelframe_widget1,
                              text=data_lang_json[lang][0]['Weather']['Min_temperature'] + " " + data["next_days"][1][
                                  'min_temp'])

        labelframe_widget2 = LabelFrame(parent_widget, text=data["next_days"][2]['name'],
                                        font=('Ethnocentric', 10, 'bold'), foreground='green')
        label_widget6 = Label(labelframe_widget2,
                              text=data_lang_json[lang][0]['Weather']['Description'] + " " + data["next_days"][2][
                                  'weather'])
        label_widget7 = Label(labelframe_widget2,
                              text=data_lang_json[lang][0]['Weather']['Max_temperature'] + " " + data["next_days"][2][
                                  'max_temp'])
        label_widget8 = Label(labelframe_widget2,
                              text=data_lang_json[lang][0]['Weather']['Min_temperature'] + " " + data["next_days"][2][
                                  'min_temp'])

        labelframe_widget3 = LabelFrame(parent_widget, text=data["next_days"][3]['name'],
                                        font=('Ethnocentric', 10, 'bold'), foreground='green')
        label_widget9 = Label(labelframe_widget3,
                              text=data_lang_json[lang][0]['Weather']['Description'] + " " + data["next_days"][3][
                                  'weather'])
        label_widget10 = Label(labelframe_widget3,
                               text=data_lang_json[lang][0]['Weather']['Max_temperature'] + " " + data["next_days"][3][
                                   'max_temp'])
        label_widget11 = Label(labelframe_widget3,
                               text=data_lang_json[lang][0]['Weather']['Min_temperature'] + " " + data["next_days"][3][
                                   'min_temp'])

        labelframe_widget4 = LabelFrame(parent_widget, text=data["next_days"][4]['name'],
                                        font=('Ethnocentric', 10, 'bold'), foreground='green')
        label_widget12 = Label(labelframe_widget4,
                               text=data_lang_json[lang][0]['Weather']['Description'] + " " + data["next_days"][4][
                                   'weather'])
        label_widget13 = Label(labelframe_widget4,
                               text=data_lang_json[lang][0]['Weather']['Max_temperature'] + " " + data["next_days"][4][
                                   'max_temp'])
        label_widget14 = Label(labelframe_widget4,
                               text=data_lang_json[lang][0]['Weather']['Min_temperature'] + " " + data["next_days"][4][
                                   'min_temp'])

        labelframe_widget5 = LabelFrame(parent_widget, text=data["next_days"][5]['name'],
                                        font=('Ethnocentric', 10, 'bold'), foreground='green')
        label_widget15 = Label(labelframe_widget5,
                               text=data_lang_json[lang][0]['Weather']['Description'] + " " + data["next_days"][5][
                                   'weather'])
        label_widget16 = Label(labelframe_widget5,
                               text=data_lang_json[lang][0]['Weather']['Max_temperature'] + " " + data["next_days"][5][
                                   'max_temp'])
        label_widget17 = Label(labelframe_widget5,
                               text=data_lang_json[lang][0]['Weather']['Min_temperature'] + " " + data["next_days"][5][
                                   'min_temp'])

        labelframe_widget6 = LabelFrame(parent_widget, text=data["next_days"][6]['name'],
                                        font=('Ethnocentric', 10, 'bold'), foreground='green')
        label_widget18 = Label(labelframe_widget6,
                               text=data_lang_json[lang][0]['Weather']['Description'] + " " + data["next_days"][6][
                                   'weather'])
        label_widget19 = Label(labelframe_widget6,
                               text=data_lang_json[lang][0]['Weather']['Max_temperature'] + " " + data["next_days"][6][
                                   'max_temp'])
        label_widget20 = Label(labelframe_widget6,
                               text=data_lang_json[lang][0]['Weather']['Min_temperature'] + " " + data["next_days"][6][
                                   'min_temp'])

        labelframe_widget7 = LabelFrame(parent_widget, text=data["next_days"][7]['name'],
                                        font=('Ethnocentric', 10, 'bold'), foreground='green')
        label_widget21 = Label(labelframe_widget7,
                               text=data_lang_json[lang][0]['Weather']['Description'] + " " + data["next_days"][7][
                                   'weather'])
        label_widget22 = Label(labelframe_widget7,
                               text=data_lang_json[lang][0]['Weather']['Max_temperature'] + " " + data["next_days"][7][
                                   'max_temp'])
        label_widget23 = Label(labelframe_widget7,
                               text=data_lang_json[lang][0]['Weather']['Min_temperature'] + " " + data["next_days"][7][
                                   'min_temp'])

        # n, ne, e, se, s, sw, w, nw,
        # -------------------------------
        # |  -  |  -  |   n    |  -  |  -  |
        # |:---:|:---:|:------:|:---:|:---:|
        # |  -  | nw  |   -    | ne  |  -  |
        # |  w  |  -  | center |  -  |  e  |
        # |  -  | sw  |   -    | se  |  -  |
        # |  -  |  -  |   s    |  -  |  -  |

        labelframe_widget.place(x=10, y=10, anchor='nw')
        labelframe_widget1.place(x=10, y=100, anchor='nw')
        labelframe_widget2.place(x=10, y=190, anchor='nw')
        labelframe_widget3.place(x=10, y=280, anchor='nw')
        labelframe_widget4.place(x=10, y=370, anchor='nw')
        labelframe_widget5.place(x=10, y=460, anchor='nw')
        labelframe_widget6.place(x=10, y=550, anchor='nw')
        labelframe_widget7.place(x=10, y=640, anchor='nw')

        label_widget0.pack()
        label_widget1.pack()
        label_widget2.pack()
        label_widget3.pack()
        label_widget4.pack()
        label_widget5.pack()
        label_widget6.pack()
        label_widget7.pack()
        label_widget8.pack()
        label_widget9.pack()
        label_widget10.pack()
        label_widget11.pack()
        label_widget12.pack()
        label_widget13.pack()
        label_widget14.pack()
        label_widget15.pack()
        label_widget16.pack()
        label_widget17.pack()
        label_widget18.pack()
        label_widget19.pack()
        label_widget20.pack()
        label_widget21.pack()
        label_widget22.pack()
        label_widget23.pack()


    def systeminfo():
        my_windows1 = tk.Tk()
        my_windows1.title(data_lang_json[lang][0]['Menu']['SystemInfo'] + " Console log")
        my_windows1.minsize(862, 455)
        my_windows1.geometry('862x455')

        log_widget = ScrolledText(my_windows1, height=30, width=120, font=("consolas", "10", "normal"))
        log_widget.pack()

        class PrintLogger(object):  # create file like object

            def __init__(self, textbox):  # pass reference to text widget
                self.textbox = textbox  # keep ref

            def write(self, text):
                self.textbox.configure(state="normal")  # make field editable
                self.textbox.insert("end", text)  # write text to textbox
                self.textbox.see("end")  # scroll to end
                self.textbox.configure(state="disabled")  # make field readonly

            def flush(self):  # needed for file like object
                pass

        logger = PrintLogger(log_widget)
        sys.stdout = logger
        sys.stderr = logger

        # ***********************************************************************
        # SYSTEM PLATFORM
        # ***********************************************************************
        def get_size(bytess, suffix="B"):
            """
            Scale bytes to its proper format
            e.g:
                1253656 => '1.20MB'
                1253656678 => '1.17GB'
            """
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytess < factor:
                    return f"{bytess:.2f}{unit}{suffix}"
                bytess /= factor

        print("=" * 40, "System Information", "=" * 40)
        uname = platform.uname()
        print(f"System: {uname.system}")
        print(f"Node Name: {uname.node}")
        print(f"Release: {uname.release}")
        print(f"Version: {uname.version}")
        print(f"Machine: {uname.machine}")
        print(f"Processor: {uname.processor}")

        # Boot Time
        print("=" * 40, "Boot Time", "=" * 40)
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

        # let's print CPU information
        print("=" * 40, "CPU Info", "=" * 40)
        # number of cores
        print("Physical cores:", psutil.cpu_count(logical=False))
        print("Total cores:", psutil.cpu_count(logical=True))
        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
        print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
        print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
        # CPU usage
        print("CPU Usage Per Core:")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            print(f"Core {i}: {percentage}%")
        print(f"Total CPU Usage: {psutil.cpu_percent()}%")

        # Memory Information
        print("=" * 40, "Memory Information", "=" * 40)
        # get the memory details
        svmem = psutil.virtual_memory()
        print(f"Total: {get_size(svmem.total)}")
        print(f"Available: {get_size(svmem.available)}")
        print(f"Used: {get_size(svmem.used)}")
        print(f"Percentage: {svmem.percent}%")
        print("=" * 20, "SWAP", "=" * 20)
        # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        print(f"Total: {get_size(swap.total)}")
        print(f"Free: {get_size(swap.free)}")
        print(f"Used: {get_size(swap.used)}")
        print(f"Percentage: {swap.percent}%")

        # Disk Information
        print("=" * 40, "Disk Information", "=" * 40)
        print("Partitions and Usage:")
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"=== Device: {partition.device} ===")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system type: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            print(f"  Total Size: {get_size(partition_usage.total)}")
            print(f"  Used: {get_size(partition_usage.used)}")
            print(f"  Free: {get_size(partition_usage.free)}")
            print(f"  Percentage: {partition_usage.percent}%")
        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        print(f"Total read: {get_size(disk_io.read_bytes)}")
        print(f"Total write: {get_size(disk_io.write_bytes)}")

        # Network information
        print("=" * 40, "Network Information", "=" * 40)
        # get all network interfaces (virtual and physical)
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                print(f"=== Interface: {interface_name} ===")
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"  IP Address: {address.address}")
                    print(f"  Netmask: {address.netmask}")
                    print(f"  Broadcast IP: {address.broadcast}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print(f"  MAC Address: {address.address}")
                    print(f"  Netmask: {address.netmask}")
                    print(f"  Broadcast MAC: {address.broadcast}")

        # get IO statistics since boot
        net_io = psutil.net_io_counters()
        print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
        print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

        # GPU information
        print("=" * 40, "GPU Details", "=" * 40)
        gpus = GPUtil.getGPUs()
        list_gpus = []
        for gpu in gpus:
            # get the GPU id
            gpu_id = gpu.id
            # name of GPU
            gpu_name = gpu.name
            # get % percentage of GPU usage of that GPU
            gpu_load = f"{gpu.load * 100}%"
            # get free memory in MB format
            gpu_free_memory = f"{gpu.memoryFree}MB"
            # get used memory
            gpu_used_memory = f"{gpu.memoryUsed}MB"
            # get total memory
            gpu_total_memory = f"{gpu.memoryTotal}MB"
            # get GPU temperature in Celsius
            gpu_temperature = f"{gpu.temperature} °C"
            gpu_uuid = gpu.uuid
            list_gpus.append((
                gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
                gpu_total_memory, gpu_temperature, gpu_uuid
            ))

        print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                           "temperature", "uuid")))


    def exits():
        # exit()
        my_windows.destroy()


    class apps:
        @staticmethod
        def apps_torrent():
            ws = Tk()
            ws.title('Torrent List')
            ws.geometry('400x300')

            def showSelected():
                countries = []
                cname = lb.curselection()
                for i in cname:
                    op = lb.get(i)
                    countries.append(op)
                for val in countries:
                    # print(val)

                    if val == "qBittorrent":
                        import webbrowser
                        webbrowser.open("https://www.qbittorrent.org/")

                    if val == "BitTorrent":
                        import webbrowser
                        webbrowser.open("https://www.bittorrent.com/")

                    if val == "Vuze":
                        import webbrowser
                        webbrowser.open("https://www.vuze.com/")

                    if val == "Deluge":
                        import webbrowser
                        webbrowser.open("https://deluge-torrent.org/")

                    if val == "Bitport.io":
                        import webbrowser
                        webbrowser.open("https://bitport.io/welcome")

                    if val == "uTorrent":
                        import webbrowser
                        webbrowser.open("https://www.utorrent.com/")

                    if val == "Tixati":
                        import webbrowser
                        webbrowser.open("https://www.tixati.com/")

                    if val == "BiglyBt":
                        import webbrowser
                        webbrowser.open("https://www.biglybt.com/")

                    if val == "Transmission":
                        import webbrowser
                        webbrowser.open("https://transmissionbt.com/")

                    if val == "WebTorrent Desktop":
                        import webbrowser
                        webbrowser.open("https://webtorrent.io/desktop/")

                    if val == "BitLord":
                        import webbrowser
                        webbrowser.open("https://www.bitlord.com/")

                    if val == "BitComet":
                        import webbrowser
                        webbrowser.open("https://www.bitcomet.com/en")

                    if val == "FrostWire":
                        import webbrowser
                        webbrowser.open("https://www.frostwire.com/")

                    if val == "ZbigZ":
                        import webbrowser
                        webbrowser.open("https://zbigz.com/")

                    if val == "Halite BitTorrent Client":
                        import webbrowser
                        webbrowser.open("https://sourceforge.net/projects/halite/")

            show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10,
                         pady=10)
            show.pack()

            lb = Listbox(ws, selectmode="multiple")
            lb.pack(padx=10, pady=10, expand=YES, fill="both")

            torrent = ["qBittorrent",
                       "BitTorrent",
                       "Vuze",
                       "Deluge",
                       "Bitport.io",
                       "uTorrent",
                       "Tixati",
                       "BiglyBt",
                       "Transmission",
                       "WebTorrent Desktop",
                       "BitLord",
                       "BitComet",
                       "FrostWire",
                       "ZbigZ",
                       "Halite BitTorrent Client"]

            for item in range(len(torrent)):
                lb.insert(END, torrent[item])
                lb.itemconfig(item, bg="#bdc1d6")

            Button(ws, text=data_lang_json[lang][0]['Weblink']['Show_Selected'], command=showSelected).pack()

        @staticmethod
        def apps_media_server():
            ws = Tk()
            ws.title('Media Server List')
            ws.geometry('400x300')

            def showSelected():
                countries = []
                cname = lb.curselection()
                for i in cname:
                    op = lb.get(i)
                    countries.append(op)
                for val in countries:
                    # print(val)

                    if val == "PlayOn":
                        import webbrowser
                        webbrowser.open("https://www.playon.tv/features?rsrc=sas&sscid=c1k6_od6ff")

                    if val == "Plex":
                        import webbrowser
                        webbrowser.open("https://www.plex.tv/")

                    if val == "Stremio":
                        import webbrowser
                        webbrowser.open("https://www.stremio.com/")

                    if val == "Emby Server":
                        import webbrowser
                        webbrowser.open("https://emby.media/")

                    if val == "OSMC":
                        import webbrowser
                        webbrowser.open("https://osmc.tv/")

                    if val == "Kodi":
                        import webbrowser
                        webbrowser.open("https://kodi.tv/")

                    if val == "Jellyfin":
                        import webbrowser
                        webbrowser.open("https://jellyfin.org/")

                    if val == "Subsonic":
                        import webbrowser
                        webbrowser.open("http://www.subsonic.org/pages/index.jsp")

                    if val == "Media Portal":
                        import webbrowser
                        webbrowser.open("https://www.team-mediaportal.com/")

                    if val == "Mezzmo":
                        import webbrowser
                        webbrowser.open("http://www.conceiva.com/products/mezzmo/")

                    if val == "TVersity":
                        import webbrowser
                        webbrowser.open("http://tversity.com/")

                    if val == "Serviio":
                        import webbrowser
                        webbrowser.open("https://serviio.org/")

                    if val == "JRiver Media Center":
                        import webbrowser
                        webbrowser.open("https://www.jriver.com/purchase.html")

                    if val == "Madsonic":
                        import webbrowser
                        webbrowser.open("https://www.madsonic.org/pages/index.jsp")

                    if val == "Imediashare":
                        import webbrowser
                        webbrowser.open("https://www.imediashare.tv/")

                    if val == "Ampache":
                        import webbrowser
                        webbrowser.open("https://ampache.org/")

            show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10,
                         pady=10)
            show.pack()

            lb = Listbox(ws, selectmode="multiple")
            lb.pack(padx=10, pady=10, expand=YES, fill="both")

            torrent = ["PlayOn",
                       "Plex",
                       "Stremio",
                       "Emby Server",
                       "OSMC",
                       "Kodi",
                       "Jellyfin",
                       "Subsonic",
                       "Media Portal",
                       "Mezzmo",
                       "TVersity",
                       "Serviio",
                       "JRiver Media Center",
                       "Madsonic",
                       "Imediashare",
                       "Ampache"]

            for item in range(len(torrent)):
                lb.insert(END, torrent[item])
                lb.itemconfig(item, bg="#bdc1d6")

            Button(ws, text=data_lang_json[lang][0]['Weblink']['Show_Selected'], command=showSelected).pack()

        @staticmethod
        def apps_video_editor():
            ws = Tk()
            ws.title('Video Editor List')
            ws.geometry('400x300')

            def showSelected():
                countries = []
                cname = lb.curselection()
                for i in cname:
                    op = lb.get(i)
                    countries.append(op)
                for val in countries:
                    # print(val)

                    if val == "Shotcut":
                        import webbrowser
                        webbrowser.open("https://shotcut.org/download/?utmzz=utmccn%3D%28not+set%29&webuid=whrz1p")

                    if val == "OpenShot Video Editor":
                        import webbrowser
                        webbrowser.open("https://www.openshot.org/download/?utmzz=utmccn%3D%28not+set%29&webuid=whrz1p")

                    if val == "DaVinci Resolve 18":
                        import webbrowser
                        webbrowser.open(
                            "https://www.blackmagicdesign.com/products/davinciresolve/"
                            "?utmzz=utmccn%3D(not%20set)&webuid=whrz1p")

                    if val == "Video Editor":
                        import webbrowser
                        webbrowser.open(
                            "https://icecreamapps.com/Video-editor/?utmzz=utmccn%3D%28not+set%29&webuid=whrz1p")

                    if val == "Digital Video Editor":
                        import webbrowser
                        webbrowser.open(
                            "https://www.nchsoftware.com/videopad/?utmzz=utmccn%3D%28not+set%29&webuid=whrz1p")

                    if val == "HitFilm":
                        import webbrowser
                        webbrowser.open("https://fxhome.com/product/hitfilm?utmzz=utmccn%3D%28not+set%29&webuid=whrz1p")

            show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10,
                         pady=10)
            show.pack()

            lb = Listbox(ws, selectmode="multiple")
            lb.pack(padx=10, pady=10, expand=YES, fill="both")

            videoeditor = ["Shotcut",
                           "OpenShot Video Editor",
                           "DaVinci Resolve 18",
                           "EVideo Editor",
                           "Digital Video Editor",
                           "HitFilm"]

            for item in range(len(videoeditor)):
                lb.insert(END, videoeditor[item])
                lb.itemconfig(item, bg="#bdc1d6")

            Button(ws, text=data_lang_json[lang][0]['Weblink']['Show_Selected'], command=showSelected).pack()


    class games:
        @staticmethod
        def game_launcher():
            ws = Tk()
            ws.title('Game Apps')
            ws.geometry('400x300')

            def showSelected():
                countries = []
                cname = lb.curselection()
                for i in cname:
                    op = lb.get(i)
                    countries.append(op)
                for val in countries:
                    # print(val)

                    if val == "Electronics Arts":
                        import webbrowser
                        webbrowser.open("https://www.ea.com/ea-app")

                    if val == "Steam":
                        import webbrowser
                        webbrowser.open("https://store.steampowered.com/")

                    if val == "Epic Games":
                        import webbrowser
                        webbrowser.open("https://www.epicgames.com/site/de/home")

                    if val == "Battle.net":
                        import webbrowser
                        webbrowser.open("https://www.blizzard.com/en-us/apps/battle.net/desktop")

                    if val == "Microsoft Game Pass":
                        import webbrowser
                        webbrowser.open("https://www.xbox.com/en-US/xbox-game-pass/pc-game-pass")

                    if val == "Ubisoft":
                        import webbrowser
                        webbrowser.open("https://ubisoftconnect.com/")

            show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10,
                         pady=10)
            show.pack()

            lb = Listbox(ws, selectmode="multiple")
            lb.pack(padx=10, pady=10, expand=YES, fill="both")

            gamess = ["Electronics Arts",
                      "Steam",
                      "Epic Games",
                      "Battle.net",
                      "Microsoft Game Pass",
                      "Ubisoft"]

            for item in range(len(gamess)):
                lb.insert(END, gamess[item])
                lb.itemconfig(item, bg="#bdc1d6")

            Button(ws, text=data_lang_json[lang][0]['Weblink']['Show_Selected'], command=showSelected).pack()


    class music:
        @staticmethod
        def music_stream():
            ws = Tk()
            ws.title('Music streaming apps')
            ws.geometry('400x300')

            def showSelected():
                global response, ROOT_DIR
                countries = []
                cname = lb.curselection()
                for i in cname:
                    op = lb.get(i)
                    countries.append(op)
                for val in countries:
                    # print(val)

                    if val == "Bandcamp":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')

                        patha = ROOT_DIR + '/Language/music_stream.json'
                        response = open(patha, encoding='utf-8')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget, text=data_lang_json[lang][0]['Music']['Bandcamp'])
                        label_widget0 = Label(labelframe_widget, text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                                      path_jsonq[data_jsonq['config_language'][0]][
                                                                          'Bandcamp']['Price'])
                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Bandcamp'][
                                                       'Audio_quality'])
                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Bandcamp'][
                                                       'Mobile_support'])
                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Bandcamp'][
                                                       'Playlisting_features'])
                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://bandcamp.com/")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

                    if val == "Tidal":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')

                        ROOT_DIR = os.path.abspath(os.curdir)
                        patha = ROOT_DIR + '/Language/music_stream.json'
                        response = open(patha, encoding='utf-8')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget,
                                                       text=data_lang_json[lang][0]['Music']['Tidal'])

                        label_widget0 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Tidal']['Price'])

                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Tidal'][
                                                       'Audio_quality'])

                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Tidal'][
                                                       'Mobile_support'])

                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Tidal'][
                                                       'Playlisting_features'])

                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://tidal.com/")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

                    if val == "Apple Music":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')

                        ROOT_DIR = os.path.abspath(os.curdir)
                        patha = ROOT_DIR + '/Language/music_stream.json'
                        response = open(patha, encoding='utf-8')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget,
                                                       text=data_lang_json[lang][0]['Music']['Apple_Music'])

                        label_widget0 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Apple_Music']['Price'])

                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Apple_Music'][
                                                       'Audio_quality'])

                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Apple_Music'][
                                                       'Mobile_support'])

                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Apple_Music'][
                                                       'Playlisting_features'])

                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://www.apple.com/apple-music/")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

                    if val == "Amazon Music Unlimited":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')

                        ROOT_DIR = os.path.abspath(os.curdir)
                        patha = ROOT_DIR + '/Language/music_stream.json'
                        response = open(patha, encoding='utf-8')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget,
                                                       text=data_lang_json[lang][0]['Music']['Amazon_Music_Unlimited'])

                        label_widget0 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]][
                                                       'Amazon_Music_Unlimited'][
                                                       'Price'])

                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]][
                                                       'Amazon_Music_Unlimited'][
                                                       'Audio_quality'])

                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]][
                                                       'Amazon_Music_Unlimited'][
                                                       'Mobile_support'])

                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]][
                                                       'Amazon_Music_Unlimited'][
                                                       'Playlisting_features'])

                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://www.amazon.com/music/prime/")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

                    if val == "Spotify":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')

                        ROOT_DIR = os.path.abspath(os.curdir)
                        patha = ROOT_DIR + '/Language/music_stream.json'
                        response = open(patha, encoding='utf-8')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget,
                                                       text=data_lang_json[lang][0]['Music']['Spotify'])

                        label_widget0 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Spotify']['Price'])

                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Spotify'][
                                                       'Audio_quality'])

                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Spotify'][
                                                       'Mobile_support'])

                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Spotify'][
                                                       'Playlisting_features'])

                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://open.spotify.com/")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

                    if val == "YouTube Music":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')

                        ROOT_DIR = os.path.abspath(os.curdir)
                        patha = ROOT_DIR + '/Language/music_stream.json'
                        response = open(patha, encoding='utf-8')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget,
                                                       text=data_lang_json[lang][0]['Music']['YouTube_Music'])

                        label_widget0 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['YouTube_Music'][
                                                       'Price'])

                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['YouTube_Music'][
                                                       'Audio_quality'])

                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['YouTube_Music'][
                                                       'Mobile_support'])

                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['YouTube_Music'][
                                                       'Playlisting_features'])

                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://music.youtube.com/")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

                    if val == "Deezer":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')

                        ROOT_DIR = os.path.abspath(os.curdir)
                        patha = ROOT_DIR + '/Language/music_stream.json'
                        response = open(patha, encoding='utf-8')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget,
                                                       text=data_lang_json[lang][0]['Music']['Deezer'])

                        label_widget0 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Deezer']['Price'])

                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Deezer'][
                                                       'Audio_quality'])

                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Deezer'][
                                                       'Mobile_support'])

                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Deezer'][
                                                       'Playlisting_features'])

                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://www.deezer.com/us/")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

                    if val == "Qobuz":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')

                        ROOT_DIR = os.path.abspath(os.curdir)
                        patha = ROOT_DIR + '/Language/music_stream.json'
                        response = open(patha, encoding='utf-8')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget,
                                                       text=data_lang_json[lang][0]['Music']['Qobuz'])

                        label_widget0 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Qobuz']['Price'])

                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Qobuz'][
                                                       'Audio_quality'])

                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Qobuz'][
                                                       'Mobile_support'])

                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Qobuz'][
                                                       'Playlisting_features'])

                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://www.qobuz.com/us-en/discover")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

                    if val == "Pandora":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')

                        ROOT_DIR = os.path.abspath(os.curdir)
                        patha = ROOT_DIR + '/Language/music_stream.json'
                        response = open(patha, encoding='utf-8')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget,
                                                       text=data_lang_json[lang][0]['Music']['Pandora'])

                        label_widget0 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Pandora']['Price'])

                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Pandora'][
                                                       'Audio_quality'])

                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Pandora'][
                                                       'Mobile_support'])

                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]]['Pandora'][
                                                       'Playlisting_features'])

                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://www.pandora.com/")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

                    if val == "SiriusXM Internet Radio":
                        parent_widget = Tk()
                        parent_widget.minsize(400, 150)
                        parent_widget.geometry('400x150')
                        path_jsonq = json.loads(response.read())

                        labelframe_widget = LabelFrame(parent_widget,
                                                       text=data_lang_json[lang][0]['Music']['SiriusXM_Internet_Radio'])

                        label_widget0 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]][
                                                       'SiriusXM_Internet_Radio'][
                                                       'Price'])

                        label_widget1 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]][
                                                       'SiriusXM_Internet_Radio'][
                                                       'Audio_quality'])

                        label_widget2 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]][
                                                       'SiriusXM_Internet_Radio'][
                                                       'Mobile_support'])

                        label_widget3 = Label(labelframe_widget,
                                              text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                                   path_jsonq[data_jsonq['config_language'][0]][
                                                       'SiriusXM_Internet_Radio'][
                                                       'Playlisting_features'])

                        labelframe_widget.pack(padx=10, pady=10)

                        def weblink():
                            import webbrowser
                            webbrowser.open("https://www.siriusxm.com/streaming")

                        Button(parent_widget, text=data_lang_json[lang][0]['Music']['Weblink'], command=weblink).pack()

                        label_widget0.pack()
                        label_widget1.pack()
                        label_widget2.pack()
                        label_widget3.pack()

            show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10,
                         pady=10)
            show.pack()

            lb = Listbox(ws, selectmode="multiple")
            lb.pack(padx=10, pady=10, expand=YES, fill="both")

            musicstream = ["Bandcamp",
                           "Tidal",
                           "Apple Music",
                           "Amazon Music Unlimited",
                           "Spotify",
                           "YouTube Music",
                           "Deezer",
                           "Qobuz",
                           "Pandora",
                           "SiriusXM Internet Radio"
                           ]

            for item in range(len(musicstream)):
                lb.insert(END, musicstream[item])
                lb.itemconfig(item, bg="#bdc1d6")

            Button(ws, text=data_lang_json[lang][0]['Weblink']['Show_Selected'], command=showSelected).pack()


    def autologin():
        url = "https://download.sysinternals.com/files/AutoLogon.zip"
        filename = "AutoLogon.zip"
        response = requests.get(url, stream=True)

        total_size = int(response.headers.get("Content-Length", 0))
        block_size = 1024

        with open(filename, "wb") as f:
            for data in tqdm(response.iter_content(block_size), total=total_size // block_size, unit="KB",
                             unit_scale=True, desc=filename):
                f.write(data)

        ROOT_DIR = os.path.abspath(os.curdir)
        with zipfile.ZipFile('AutoLogon.zip', 'r') as myzip:
            myzip.extractall(path=ROOT_DIR + '\Temp\Autologin')

        os.startfile(ROOT_DIR + "\Temp\Autologin")

        ###########################################

        import tkinter.messagebox as messagebox

        while True:
            result = messagebox.showwarning("Figyelem",
                                            "Inditsad el a megfelelö fäjlt a fojtatäshoz, addig ne nyomj ok gombot")
            if result == "ok":
                def is_running(process_names):

                    running_processes = []
                    for proc in psutil.process_iter():
                        try:
                            for process_name in process_names:
                                if process_name.lower() in proc.name().lower():
                                    running_processes.append(process_name)
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            pass
                    return running_processes

                processes_to_check = ["Autologon.exe", "Autologon64.exe", "Autologon64a.exe"]
                running_processes = is_running(processes_to_check)

                if running_processes:
                    print("The following processes are running: ", running_processes)
                    result = subprocess.run(
                        ["powershell", "Start-Process", "-Verb", "runAs", "-FilePath", "python", "-ArgumentList",
                         "autologin_procc.py"],
                        stdout=subprocess.PIPE)
                    break
                else:
                    print("None of the processes are running")

        ###########################################


    # **************************************************************************************************
    # TOP GUI

    verzions()
    clock()

    my_dropdown_menu_utils = tk.Menu(my_menubar, tearoff=0)
    my_dropdown_menu_utils.add_command(label=data_lang_json[lang][0]['Menu']['virus_scann'],
                                       command=microsoft_apps.virus_scann)
    my_dropdown_menu_utils.add_command(label=data_lang_json[lang][0]['Menu']['Autologin'], command=autologin)
    my_dropdown_menu_utils.add_command(label=data_lang_json[lang][0]['Menu']['SystemInfo'], command=systeminfo)
    my_dropdown_menu_utils.add_command(label=data_lang_json[lang][0]['Menu']['Weather'], command=weather_google)
    my_menubar.add_cascade(label=data_lang_json[lang][0]['Menu']['utilities'], menu=my_dropdown_menu_utils)

    my_dropdown_menu_apps = tk.Menu(my_menubar, tearoff=0)
    my_dropdown_menu_apps.add_command(label=data_lang_json[lang][0]['Apps']['Apps_Torrent'], command=apps.apps_torrent)
    my_dropdown_menu_apps.add_command(label=data_lang_json[lang][0]['Apps']['Apps_Media_Server'],
                                      command=apps.apps_media_server)
    my_dropdown_menu_apps.add_command(label=data_lang_json[lang][0]['Apps']['Apps_Video_Editor'],
                                      command=apps.apps_video_editor)
    my_menubar.add_cascade(label=data_lang_json[lang][0]['Apps']['Apps'], menu=my_dropdown_menu_apps)

    my_dropdown_menu_games = tk.Menu(my_menubar, tearoff=0)
    my_dropdown_menu_games.add_command(label=data_lang_json[lang][0]['Games']['Game_Launcher'],
                                       command=games.game_launcher)
    my_menubar.add_cascade(label=data_lang_json[lang][0]['Games']['Games'], menu=my_dropdown_menu_games)

    my_dropdown_menu_music = tk.Menu(my_menubar, tearoff=0)
    my_dropdown_menu_music.add_command(label=data_lang_json[lang][0]['Music']['Music_list'], command=music.music_stream)
    my_menubar.add_cascade(label=data_lang_json[lang][0]['Music']['Music'], menu=my_dropdown_menu_music)

    my_dropdown_menu_help = tk.Menu(my_menubar, tearoff=0)
    my_dropdown_menu_help.add_command(label=data_lang_json[lang][0]['Menu']['Configure'], command=configure)
    my_dropdown_menu_help.add_command(label=data_lang_json[lang][0]['Menu']['Exit'], command=exits)
    my_menubar.add_cascade(label=data_lang_json[lang][0]['Menu']['Help'], menu=my_dropdown_menu_help)

    my_windows.config(menu=my_menubar)

    # *********************************************************************************
    # Hidden - Show MENU
    # *********************************************************************************

    if data_jsonq['hidde_show']['my_dropdown_menu_music'] == "Show":
        pass
    if data_jsonq['hidde_show']['my_dropdown_menu_music'] == "Hidden":
        my_menubar.entryconfig(data_lang_json[lang][0]['Music']['Music'], state="disabled")
        my_menubar.delete(data_lang_json[lang][0]['Music']['Music'])

    if data_jsonq['hidde_show']['my_dropdown_menu_games'] == "Show":
        pass
    if data_jsonq['hidde_show']['my_dropdown_menu_games'] == "Hidden":
        my_menubar.entryconfig(data_lang_json[lang][0]['Games']['Games'], state="disabled")
        my_menubar.delete(data_lang_json[lang][0]['Games']['Games'])

    if data_jsonq['hidde_show']['my_dropdown_menu_apps'] == "Show":
        pass
    if data_jsonq['hidde_show']['my_dropdown_menu_apps'] == "Hidden":
        my_menubar.entryconfig(data_lang_json[lang][0]['Apps']['Apps'], state="disabled")
        my_menubar.delete(data_lang_json[lang][0]['Apps']['Apps'])

    if data_jsonq['hidde_show']['my_dropdown_menu_utils'] == "Show":
        pass
    if data_jsonq['hidde_show']['my_dropdown_menu_utils'] == "Hidden":
        my_menubar.entryconfig(data_lang_json[lang][0]['Menu']['utilities'], state="disabled")
        my_menubar.delete(data_lang_json[lang][0]['Menu']['utilities'])

    # *********************************************************************************

    my_windows.mainloop()

else:
    my_windows.destroy()
    langs = (data_jsonq['config_error_language'][0])

    ROOT_DIR = os.path.abspath(os.curdir)
    language = ROOT_DIR + '/Language/' + langs + '.json'
    response = open(language, encoding='utf-8')

    data_lang_json = json.loads(response.read())
    messagebox.showwarning(data_lang_json[langs][0]['Messages']['Messages'],
                           "'" + lang + "'" + data_lang_json[langs][0]['Messages']['Messages_language_error'])
