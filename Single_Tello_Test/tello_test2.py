from tello import Tello
import sys
from datetime import datetime
import time

start_time = str(datetime.now())

file_name = sys.argv[1]
ip_file_name = sys.argv[2]
print(file_name)

f = open(file_name, "r")
commands = f.readlines()
f.close

ip_f = open(ip_file_name, "r")
ips = ip_f.readlines()
ips = [ip.rstrip("\n") for ip in ips]  # 改行コード削除
ip_f.close

try:
    tello = Tello(ips)  # txtファイルのipをリスト化して与える
    print(tello)
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()

            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print

                ('delay %s' % sec)
                time.sleep(sec)
                pass
            else:
                tello.send_command(command)

        log = tello.get_log()

        out = open('log/' + start_time + '.txt', 'w')
        for stat in log:
            stat.print_stats()
            str = stat.return_stats()
            out.write(str)


except KeyboardInterrupt:
    tello.send_command("command")
    # tello.send_command("land")
    tello.send_command("emergency")
