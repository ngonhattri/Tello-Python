import socket
import threading
import time
from stats import Stats


class Tello:
    def __init__(self, ip):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        print(self.socket)
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_adderss = []  # (ip,port)を格納するリスト
        print(len(ip))

        for i in range(len(ip)):  # ipの数だけリストにip,portを格納
            self.tello_ip = ip[i]
            self.tello_port = 8889

            self.tello_adderss.append((self.tello_ip, self.tello_port))
            # name = "self.tello_adderss{} = {}".format(i,(self.tello_ip, self.tello_port))
            # exec(name)
            # print(name)

            self.log = []

            self.MAX_TIME_OUT = 15.0

    def send_command(self, command):
        """
        Send a command to the ip address. Will be blocked until
        the last command receives an 'OK'.
        If the command fails (either b/c time out or error),
        will try to resend the command
        :param command: (str) the comman
        d to send
        :param ip: (str) the ip of Tello
        :return: The latest command response
        """
        print("--------------------")
        print(command)
        print(self.tello_adderss)
        print("--------------------")

        def play_commands(address):  # 引数にtello_address(どのipのどのポートに送るか)を指定する関数
            self.socket.sendto(command.encode('utf-8'), address)

        self.log.append(Stats(command, len(self.log)))

        threads = []  # 同時実行したいスレッドを入れる
        for i in self.tello_adderss:  # リストself.tello_addressの数だけthreadsに格納
            threads.append(threading.Thread(
                target=play_commands, args=(i,), name=i))
            print(i)
            print(threads)
        for thread in threads:  # スレッド開始
            thread.start()

        for thread in threads:  # スレッドが終わるまで待機
            thread.join()

    def _receive_thread(self):
        """Listen to responses from the Tello.
        Runs as a thread, sets self.response to whatever the Tello last returned.
        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print('from %s: %s' % (ip, self.response))

                self.log[-1].add_response(self.response)
            except socket.error as exc:
                print("Caught exception socket.error : %s" % exc)

    def on_close(self):
        pass
        # for ip in self.tello_ip_list:
        #     self.socket.sendto('land'.encode('utf-8'), (ip, 8889))
        # self.socket.close()

    def get_log(self):
        return self.log
