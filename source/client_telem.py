import socket
import logging
import time
from icecream import ic


#class for communication with device
class client_telem:
    def __init__(self, ip_addr='0.0.0.0', port=9090):
        self.host = (ip_addr, port)
        self.telem = [{"state": 0, "current": 0.0,  "voltage": 0.0, "power": 0.0} for i in range(4)]
        logging.basicConfig(level=logging.INFO, filename="source/logger.log",filemode="w+",
            format="%(asctime)s %(levelname)s %(message)s")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

    async def turn_on(self, data: tuple):#on source

        #data to commands
        idx, v, i = data
        set_current = f':SOURce{idx}:CURRent {i}\n'
        set_voltage = f':SOURce{idx}:VOLTage {v}\n'
        output = f":OUTPut{idx}:STATe ON\n"
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(self.host)
            self.s.send(set_current.encode())
            self.s.send(set_voltage.encode())
            self.s.send(output.encode())
            self.s.close()
        except:
            print('No connection to server...')


    async def turn_off(self, data: int): #off source

        #data to commands
        idx = data
        output = f":OUTPut{idx}:STATe OFF\n"
        measure = f':MEASure{idx}:ALL?\n'

        try:#to device
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(self.host)
            self.s.send(output.encode())
            self.s.send(measure.encode())
            self.s.close()

            self.telem[idx]['state'] = 0
        except:
            print('No connection to server...')
        return 'turn_off'

    
    def get_data(self, ch: int): #single request
        ic('connecting')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.host)
        self.s.send(f':MEASure{ch}:ALL?\n'.encode())
        data = self.s.recv(2056).decode()
        self.s.close()
        i, v, p = data.split()
        self.telem[ch]['current'] = float(i)
        self.telem[ch]['voltage'] = float(v)
        self.telem[ch]['power'] = float(p)
    
    def collect_telem(self): #telemetry request   
        try:
            for i in range(4):
                self.get_data(i)
                print(f'data: {self.telem}')
                logging.info(f'data: {self.telem}')
        except:
            print("No connection to server...")
        time.sleep(1)

    def get_telem(self):
        return self.telem