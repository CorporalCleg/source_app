import socket
import logging
import threading
import time
# from icecream import ic

#class for communication with device
class client_telem:
    def __init__(self, ip_addr='0.0.0.0', port=9091):

        self.host = (ip_addr, port)
        self.telem = [{"state": 0, "current": 0.0,  "voltage": 0.0, "power": 0.0} for i in range(4)]
        logging.basicConfig(level=logging.INFO, filename="logger.log",filemode="w",
            format="%(asctime)s %(levelname)s %(message)s")
        
        self.t = threading.Thread(target=self.write_telem)
        self.t.start()


    def turn_on(self, data: tuple):#on source

        #data to commands
        idx, v, i = data
        set_current = f':SOURce{idx}:CURRent {i}\n'
        set_voltage = f':SOURce{idx}:VOLTage {v}\n'
        output = f":OUTPut{idx}:STATe ON\n"

        try:#to device
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.host)
                s.send(set_current.encode())
                s.send(set_voltage.encode())
                s.send(output.encode())

                self.telem[idx]['state'] = 1
        except:
            print('No connection to server...')

    def turn_off(self, data: int): #off source

        #data to commands
        idx = data
        output = f":OUTPut{idx}:STATe OFF\n"
        measure = f':MEASure{idx}:ALL?\n'

        try:#to device
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.host)
                s.send(output.encode())
                s.send(measure.encode())

                self.telem[idx]['state'] = 0

        except:
            print('No connection to server...')

    
    def get_data(self, ch: int): #single request
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.host)

            s.send(f':MEASure{ch}:ALL?\n'.encode())
            data = s.recv(2056).decode()
            i, v, p = [float(x) for x in data.split()]
            self.telem[ch]['current'] = i
            self.telem[ch]['voltage'] = v
            self.telem[ch]['power'] = p
        return (i, v, p)
    
    
    def write_telem(self): #telemetry request

        while True:    
            try:
                for i in range(4):
                    self.get_data(i)
                    logging.info(f'data: {self.telem}')
            except:
                #print("No connection to server...")
                pass
            time.sleep(1)