import json
import tkinter as tk
import os

import pytz
import sys
# import subprocess
import requests
import psutil
import platform
import GPUtil
from tabulate import tabulate

# from datetime import datetime
from bs4 import BeautifulSoup as bs
from tkinter import *
from tkinter import messagebox
from tkinter import Tk, Button
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

my_windows = tk.Tk()
my_windows.title('WindowsGuiPY')
my_windows.minsize(700, 400)
my_windows.geometry('800x400')
my_menubar = tk.Menu(my_windows)


ROOT_DIR = os.path.abspath(os.curdir)
response = open('config.json', encoding='utf-8')
data_jsonq = json.loads(response.read())
lang = (data_jsonq['config_language'][0])


path = ROOT_DIR + '/Language/' + lang + '.json'
isFile = os.path.isfile(path)

if isFile:
    language = ROOT_DIR + '/Language/' + lang + '.json'
    response = open(language, encoding='utf-8')

else:
    messagebox.showwarning("Warning", "'" + lang + "'" + " Language File Not Found!!!")


data_lang_json = json.loads(response.read())

# script
app_configure = ROOT_DIR + " "


def configure():
    import subprocess as sp
    programName = "notepad.exe"
    fileName = ROOT_DIR + "/config.json"
    sp.Popen([programName, fileName])


def clock():
    dd = (''.join(data_jsonq['timezone'][0]))
    date_time = datetime.now(pytz.timezone(dd)).strftime("%d-%m-%Y %H:%M:%S/%p")
    date, time1 = date_time.split()
    time2, time3 = time1.split('/')
    hour, minutes, seconds = time2.split(':')

    if int(hour) > 11 and int(hour) < 24:

        time = str(int(hour) - 12) + ':' + minutes + ':' + seconds + ' ' + time3
    else:
        time = time2 + ' ' + time3
    time_label.config(text=time)
    date_label.config(text=date)
    time_label.after(1000, clock)


date_label = tk.Label(my_windows, font=('calibri 30 bold', 10, 'bold'), foreground='black')
time_label = tk.Label(my_windows, font=('calibri 30 bold', 30, 'bold'), foreground='black')
date_label.place(relx=0.5, rely=0.54, anchor='center')
time_label.place(relx=0.5, rely=0.45, anchor='center')

def verzion():
    import json, requests
    url = requests.get("https://api.github.com/repos/LexyGuru/MyApps/releases")
    text = url.text
    data = json.loads(text)
    datas = data[0]


    def verzion_ch():
        pass

    response = open('config.json', encoding='utf-8')
    data_jsonq = json.loads(response.read())
    __verch__ = (data_jsonq['verzion'])

    if __verch__ == datas['name']:
        # n, ne, e, se, s, sw, w, nw,
        # -------------------------------
        # |  -  |  -  |   n    |  -  |  -  |
        # |:---:|:---:|:------:|:---:|:---:|
        # |  -  | nw  |   -    | ne  |  -  |
        # |  w  |  -  | center |  -  |  e  |
        # |  -  | sw  |   -    | se  |  -  |
        # |  -  |  -  |   s    |  -  |  -  |

        menu_label_0 = tk.Label(my_windows, text=datas['zipball_url'], font=('Ethnocentric', 8))
        menu_label_1 = tk.Label(my_windows, text=datas['published_at'], font=('Ethnocentric', 8, 'bold'))
        menu_label_2 = tk.Label(my_windows, text=datas['name'], font=('Ethnocentric', 8, 'bold'))

        menu_label_0.place(relx=0.5, rely=1.0, anchor='s')
        menu_label_1.place(relx=1, rely=1, anchor='se')
        menu_label_2.place(relx=0.0, rely=1.0, anchor='sw')

    if __verch__ < datas['name']:

        menu_label_0 = tk.Label(my_windows, text=datas['zipball_url'], font=('Ethnocentric', 8), foreground='red')
        menu_label_1 = tk.Label(my_windows, text=datas['published_at'], font=('Ethnocentric', 8, 'bold'), foreground='red')
        menu_label_2 = tk.Label(my_windows, text=datas['name'], font=('Ethnocentric', 8, 'bold'), foreground='red')

        menu_label_0.place(relx=0.5, rely=1.0, anchor='s')
        menu_label_1.place(relx=1, rely=1, anchor='se')
        menu_label_2.place(relx=0.0, rely=1.0, anchor='sw')

        uppdate = tk.Label(my_windows, text="NEW UPDATE", font=('Ethnocentric', 25, 'bold'), foreground='red')
        uppdate.place(relx=0.5, rely=0.54, anchor='center')

    if __verch__ > datas['name']:
        print('Error')

def weather_google():
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
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
        result = {}
        # extract region
        result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
        # extract temperature now
        result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
        # get the day and hour now
        result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
        # get the actual weather
        result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
        # get the precipitation
        result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
        # get the % of humidity
        result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
        # extract the wind
        result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text
        # get next few days' weather
        next_days = []
        days = soup.find("div", attrs={"id": "wob_dp"})
        for day in days.findAll("div", attrs={"class": "wob_df"}):
            # extract the name of the day
            day_name = day.findAll("div")[0].attrs['aria-label']
            # get weather status for that day
            weather = day.find("img").attrs["alt"]
            temp = day.findAll("span", {"class": "wob_t"})
            # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
            max_temp = temp[0].text
            # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
            min_temp = temp[2].text
            next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
        # append to result
        result['next_days'] = next_days
        return result

    if __name__ == "__main__":
        URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather+" + locat
        import argparse
        parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
        parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                            Default is your current location determined by your IP Address""",
                            default="")
        # parse arguments
        args = parser.parse_args()
        region = args.region
        if region:
            region = region.replace(" ", "+")
            URL += f"+{region}"
        # get data
        data = get_weather_data(URL)
        # print data

        my_windows = tk.Tk()
        my_windows.title(data_jsonq['locations'][0] + " Console log")
        my_windows.minsize(862, 455)
        my_windows.geometry('862x455')

        log_widget = ScrolledText(my_windows, height=30, width=120, font=("calibri", 12,  "bold", "normal"))
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

        print(data_lang_json[lang][0]['Weather']['Weather_for'], data["region"])
        print(data_lang_json[lang][0]['Weather']['Now'], data["dayhour"])
        print(data_lang_json[lang][0]['Weather']['Temperature_now'], f"{data['temp_now']}°C")
        print(data_lang_json[lang][0]['Weather']['Description'],data['weather_now'])
        print(data_lang_json[lang][0]['Weather']['Precipitation'],data["precipitation"])
        print(data_lang_json[lang][0]['Weather']['Humidity'],data["humidity"])
        print(data_lang_json[lang][0]['Weather']['Wind'],data["wind"])
        print(data_lang_json[lang][0]['Weather']['Next_days'])


        for dayweather in data["next_days"]:
            print("\r")
            print("=" * 40, dayweather["name"], "=" * 40)
            print(data_lang_json[lang][0]['Weather']['Description'], dayweather["weather"])
            print(data_lang_json[lang][0]['Weather']['Max_temperature'], f"{dayweather['max_temp']}°C")
            print(data_lang_json[lang][0]['Weather']['Min_temperature'], f"{dayweather['min_temp']}°C")


def systeminfo():
    my_windows = tk.Tk()
    my_windows.title(data_lang_json[lang][0]['Menu']['SystemInfo'] + " Console log")
    my_windows.minsize(862, 455)
    my_windows.geometry('862x455')

    log_widget = ScrolledText(my_windows, height=30, width=120, font=("consolas", "10", "normal"))
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
    def get_size(bytes, suffix="B"):
        """
        Scale bytes to its proper format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

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
    exit()


class apps:
    @staticmethod
    def apps_torrent():
        ws = Tk()
        ws.title('Torrent List')
        ws.geometry('400x300')

        var = StringVar()

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

        show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10, pady=10)
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

        var = StringVar()

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

        show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10, pady=10)
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

        var = StringVar()

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
                        "https://www.blackmagicdesign.com/products/davinciresolve/?utmzz=utmccn%3D(not%20set)&webuid=whrz1p")

                if val == "Video Editor":
                    import webbrowser
                    webbrowser.open("https://icecreamapps.com/Video-editor/?utmzz=utmccn%3D%28not+set%29&webuid=whrz1p")

                if val == "Digital Video Editor":
                    import webbrowser
                    webbrowser.open("https://www.nchsoftware.com/videopad/?utmzz=utmccn%3D%28not+set%29&webuid=whrz1p")

                if val == "HitFilm":
                    import webbrowser
                    webbrowser.open("https://fxhome.com/product/hitfilm?utmzz=utmccn%3D%28not+set%29&webuid=whrz1p")

        show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10, pady=10)
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

        var = StringVar()

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

        show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10, pady=10)
        show.pack()

        lb = Listbox(ws, selectmode="multiple")
        lb.pack(padx=10, pady=10, expand=YES, fill="both")

        games = ["Electronics Arts",
                   "Steam",
                   "Epic Games",
                   "Battle.net",
                   "Microsoft Game Pass",
                   "Ubisoft"]

        for item in range(len(games)):
            lb.insert(END, games[item])
            lb.itemconfig(item, bg="#bdc1d6")

        Button(ws, text=data_lang_json[lang][0]['Weblink']['Show_Selected'], command=showSelected).pack()

class music:
    @staticmethod
    def music_stream():
        ws = Tk()
        ws.title('Music streaming apps')
        ws.geometry('400x300')

        var = StringVar()

        def showSelected():
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

                    ROOT_DIR = os.path.abspath(os.curdir)
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
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
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
                    path_jsonq = json.loads(response.read())

                    labelframe_widget = LabelFrame(parent_widget,
                        text=data_lang_json[lang][0]['Music']['Tidal'])

                    label_widget0 = Label(labelframe_widget,
                        text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                        path_jsonq[data_jsonq['config_language'][0]]['Tidal']['Price'])

                    label_widget1 = Label(labelframe_widget,
                        text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                        path_jsonq[data_jsonq['config_language'][0]]['Tidal']['Audio_quality'])

                    label_widget2 = Label(labelframe_widget,
                        text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                        path_jsonq[data_jsonq['config_language'][0]]['Tidal']['Mobile_support'])

                    label_widget3 = Label(labelframe_widget,
                        text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                        path_jsonq[data_jsonq['config_language'][0]]['Tidal']['Playlisting_features'])

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
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
                    path_jsonq = json.loads(response.read())

                    labelframe_widget = LabelFrame(parent_widget,
                                                   text=data_lang_json[lang][0]['Music']['Apple_Music'])

                    label_widget0 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Apple_Music']['Price'])

                    label_widget1 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Apple_Music']['Audio_quality'])

                    label_widget2 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Apple_Music']['Mobile_support'])

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
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
                    path_jsonq = json.loads(response.read())

                    labelframe_widget = LabelFrame(parent_widget,
                                                   text=data_lang_json[lang][0]['Music']['Amazon_Music_Unlimited'])

                    label_widget0 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Amazon_Music_Unlimited']['Price'])

                    label_widget1 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Amazon_Music_Unlimited']['Audio_quality'])

                    label_widget2 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Amazon_Music_Unlimited']['Mobile_support'])

                    label_widget3 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Amazon_Music_Unlimited'][
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
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
                    path_jsonq = json.loads(response.read())

                    labelframe_widget = LabelFrame(parent_widget,
                                                   text=data_lang_json[lang][0]['Music']['Spotify'])

                    label_widget0 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Spotify']['Price'])

                    label_widget1 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Spotify']['Audio_quality'])

                    label_widget2 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Spotify']['Mobile_support'])

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
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
                    path_jsonq = json.loads(response.read())

                    labelframe_widget = LabelFrame(parent_widget,
                                                   text=data_lang_json[lang][0]['Music']['YouTube_Music'])

                    label_widget0 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['YouTube_Music']['Price'])

                    label_widget1 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['YouTube_Music']['Audio_quality'])

                    label_widget2 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['YouTube_Music']['Mobile_support'])

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
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
                    path_jsonq = json.loads(response.read())

                    labelframe_widget = LabelFrame(parent_widget,
                                                   text=data_lang_json[lang][0]['Music']['Deezer'])

                    label_widget0 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Deezer']['Price'])

                    label_widget1 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Deezer']['Audio_quality'])

                    label_widget2 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Deezer']['Mobile_support'])

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
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
                    path_jsonq = json.loads(response.read())

                    labelframe_widget = LabelFrame(parent_widget,
                                                   text=data_lang_json[lang][0]['Music']['Qobuz'])

                    label_widget0 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Qobuz']['Price'])

                    label_widget1 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Qobuz']['Audio_quality'])

                    label_widget2 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Qobuz']['Mobile_support'])

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
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
                    path_jsonq = json.loads(response.read())

                    labelframe_widget = LabelFrame(parent_widget,
                                                   text=data_lang_json[lang][0]['Music']['Pandora'])

                    label_widget0 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Pandora']['Price'])

                    label_widget1 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Pandora']['Audio_quality'])

                    label_widget2 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['Pandora']['Mobile_support'])

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

                    ROOT_DIR = os.path.abspath(os.curdir)
                    path = ROOT_DIR + '/Language/music_stream.json'
                    response = open(path, encoding='utf-8')
                    path_jsonq = json.loads(response.read())

                    labelframe_widget = LabelFrame(parent_widget,
                                                   text=data_lang_json[lang][0]['Music']['SiriusXM_Internet_Radio'])

                    label_widget0 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Price'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['SiriusXM_Internet_Radio']['Price'])

                    label_widget1 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Audio_quality'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['SiriusXM_Internet_Radio']['Audio_quality'])

                    label_widget2 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Mobile_support'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['SiriusXM_Internet_Radio']['Mobile_support'])

                    label_widget3 = Label(labelframe_widget,
                                          text=data_lang_json[lang][0]['Music']['Playlisting_features'] + ": " +
                                               path_jsonq[data_jsonq['config_language'][0]]['SiriusXM_Internet_Radio'][
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


        show = Label(ws, text=data_lang_json[lang][0]['Weblink']['Select_Your_Apps'], font=("Times", 14), padx=10, pady=10)
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

verzion()
clock()

my_dropdown_menu_utils = tk.Menu(my_menubar, tearoff=0)
my_dropdown_menu_utils.add_command(label=data_lang_json[lang][0]['Menu']['SystemInfo'], command=systeminfo)
my_dropdown_menu_utils.add_command(label=data_lang_json[lang][0]['Menu']['Weather'], command=weather_google)
my_menubar.add_cascade(label=data_lang_json[lang][0]['Menu']['utilities'], menu=my_dropdown_menu_utils)

my_dropdown_menu_apps = tk.Menu(my_menubar, tearoff=0)
my_dropdown_menu_apps.add_command(label=data_lang_json[lang][0]['Apps']['Apps_Torrent'], command=apps.apps_torrent)
my_dropdown_menu_apps.add_command(label=data_lang_json[lang][0]['Apps']['Apps_Media_Server'], command=apps.apps_media_server)
my_dropdown_menu_apps.add_command(label=data_lang_json[lang][0]['Apps']['Apps_Video_Editor'], command=apps.apps_video_editor)
my_menubar.add_cascade(label=data_lang_json[lang][0]['Apps']['Apps'], menu=my_dropdown_menu_apps)

my_dropdown_menu_games = tk.Menu(my_menubar, tearoff=0)
my_dropdown_menu_games.add_command(label=data_lang_json[lang][0]['Games']['Game_Launcher'], command=games.game_launcher)
my_menubar.add_cascade(label=data_lang_json[lang][0]['Games']['Games'], menu=my_dropdown_menu_games)

my_dropdown_menu_music = tk.Menu(my_menubar, tearoff=0)
my_dropdown_menu_music.add_command(label=data_lang_json[lang][0]['Music']['Music_list'], command=music.music_stream)
my_menubar.add_cascade(label=data_lang_json[lang][0]['Music']['Music'], menu=my_dropdown_menu_music)

my_dropdown_menu_help = tk.Menu(my_menubar, tearoff=0)
my_dropdown_menu_help.add_command(label=data_lang_json[lang][0]['Menu']['Configure'], command=configure)
my_dropdown_menu_help.add_command(label=data_lang_json[lang][0]['Menu']['Exit'], command=exits)
my_menubar.add_cascade(label=data_lang_json[lang][0]['Menu']['Help'], menu=my_dropdown_menu_help)

my_windows.config(menu=my_menubar)
my_windows.mainloop()
