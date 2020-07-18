import time
import threading
import sys
import urllib.request, json
import schedule
import datetime

class Meteo_PJD:
    "Fetch JSON dictionnary with weather data from PJD sensor"

    chalet_plageURL = "https://backend.visionmeteo.com/API/ParcJeanDrapeau/7XvlQtPkltlJUZJt/chaletplage"
    history = [None, None]

    def fetch(self):
        with urllib.request.urlopen(self.chalet_plageURL) as url:
            self.sensors = json.loads(url.read().decode())

    def initial_data(self):
        self.history[0] = self.sensors["TempAir"]
        sys.stdout.write("\033[F") #back to previous line
        sys.stdout.write("\033[K") #clear line
        print('Chalet de la plage -', self.sensors["DateHeure"], '- Température', self.sensors["TempAir"],'°C', end='\r')

    def update_interval(self):
        epoch = int(time.time())
        time_storage = [epoch, 0]
        oldTS = self.sensors["DateHeure"]
        while oldTS == self.sensors["DateHeure"]:
            self.fetch()
            epoch = int(time.time())
            time_storage[1] = epoch
            time.sleep(1)
        self.update_timing = int(time_storage[1] - time_storage[0])
        if self.history[0] == None:
            t1 = threading.Thread(target=self.update_timer)
            t1.start()
        else:
            pass

    def update_timer(self):
        self.show_data()
        schedule.every(self.update_timing).seconds.do(self.fetch)
        schedule.every(self.update_timing).seconds.do(self.show_data)
        schedule.every(120).minutes.do(self.update_interval)
        # print("Wainting", self.update_timing)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def show_data(self):
        self.history.append(self.history.pop(0))
        self.history[0] = self.sensors["TempAir"]
        self.new = self.history[0]
        self.old = self.history[1]
        #print("Temp sensors history", self.new, self.old)
        if self.old == None:
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
            print('Mise à jour:', self.update_timing, 'sec -', 'Chalet de la plage -', self.sensors["DateHeure"], '- Température', self.sensors["TempAir"],'°C', end='\r')
        elif self.old > self.new:
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
            print('Mise à jour:', self.update_timing, 'sec -', 'Chalet de la plage -', self.sensors["DateHeure"], '- Température', self.sensors["TempAir"],'°C ▼', end='\r')
        elif self.old < self.new:
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
            print('Mise à jour:', self.update_timing, 'sec -', 'Chalet de la plage -', self.sensors["DateHeure"], '- Température', self.sensors["TempAir"],'°C ▲', end='\r')
        else:
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
            print('Mise à jour:', self.update_timing, 'sec -', 'Chalet de la plage -', self.sensors["DateHeure"], '- Température', self.sensors["TempAir"],'°C ▲▼', end='\r')

temp = Meteo_PJD()
temp.fetch()
temp.initial_data()
temp.update_interval()
