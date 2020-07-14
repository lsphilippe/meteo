import time
import threading
import sys
import urllib.request, json
import schedule

def fetch():
    urlCP = "https://backend.visionmeteo.com/API/ParcJeanDrapeau/7XvlQtPkltlJUZJt/chaletplage"
    with urllib.request.urlopen(urlCP) as url:
        dict = json.loads(url.read().decode())
        return dict

def timing():
    clock = int(time.time())
    tstamp = [0, 0]
    dict["DateHeure"] = tstamp[0]
    dict["DateHeure"] = tstamp[1]
    while True:
        fetch(dict)
        if tstamp[0] == tstamp[1]:
            data()
        else:
            dict["DateHeure"] = tstamp[1]
            if tstamp[1] != tstamp[0]:
            clock_diff = int(time.time()) - clock
            schedule.every(clock_diff).minutes.do(print)
            break

def print():
    fetch(dict)
    meteo = [None, None]
    epoch = [None, None]

    epoch.append(epoch.pop(0))
    epoch[0] = dict["DateHeure"]
    new_epoch = epoch[0]
    old_epoch = epoch[1]

    meteo.append(meteo.pop(0))
    meteo[0] = dict["TempAir"]
    new = meteo[0]
    old = meteo[1]

    if new_epoch == old_epoch:
        pass
    else:
        if old == None:
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
            print('Chalet de la plage -', dict["DateHeure"], '- Température', new,'°C', end='\r')
        elif old > new:
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
            print('Chalet de la plage -', dict["DateHeure"], '- Température', new,'°C ▼', end='\r')
        elif old < new:
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
            print('Chalet de la plage -', dict["DateHeure"], '- Température', new,'°C ▲', end='\r')
        else:
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
            print('Chalet de la plage -', dict["DateHeure"], '- Température', new,'°C ▲▼', end='\r')

def main():
    while True:
        key = input()
        if key == 'x':
            # t1.do_run = False
            # t1.join
            sys.exit("Exiting...")
        else:
            pass

main()
