#Grott Growatt monitor :  Proxy 
#       
# Updated: 2022-08-07
# Version 2.7.5

import threading
import socket
import select
import time
import sys
import struct
import textwrap
from itertools import cycle # to support "cycling" the iterator
import time, json, datetime, codecs
## to resolve errno 32: broken pipe issue (only linux)
if sys.platform != 'win32' :
   from signal import signal, SIGPIPE, SIG_DFL

from datetime import datetime

from grottdata import procdata, decrypt, format_multi_line

#import mqtt                       
import paho.mqtt.publish as publish

#import libscrc for additional crc checking                        
# for compat reason (generate a message in the log) also done in proxy _init_
try:     
    import libscrc
except:
    print("\t **********************************************************************************")
    print("\t - Grott - libscrc not installed, no CRC checking only record validation on length!") 
    print("\t **********************************************************************************")


# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
#buffer_size = 65535
delay = 0.0002

def validate_record(xdata): 
    # validata data record on length and CRC (for "05" and "06" records)
    
    data = bytes.fromhex(xdata)
    ldata = len(data)
    len_orgpayload = int.from_bytes(data[4:6],"big")
    header = "".join("{:02x}".format(n) for n in data[0:8])
    protocol = header[6:8]

    if protocol in ("05","06"):
        lcrc = 4
        crc = int.from_bytes(data[ldata-2:ldata],"big")
    else: 
        lcrc = 0

    len_realpayload = (ldata*2 - 12 -lcrc) / 2

    if protocol != "02" :
                
        try: 
            crc_calc = libscrc.modbus(data[0:ldata-2])
        except: 
            #liscrc is not installed yet
            #print("\t - Grott - Validate datarecord - libscrc not installed, only validation on record length")  
            crc_calc = crc = 0 

    if len_realpayload == len_orgpayload :
        returncc = 0
        if protocol != "02" and crc != crc_calc:     
            returncc = 8    
    else : 
        returncc = 8

    return(returncc)


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.forward.settimeout(5)

    def start(self, host, port):
        # fallback forwarding to grottserver if remote server is unreachable
        # if not forward:
        #     print("\t - Can't establish connection growatt server, attempting to fall back to local grott server.")
        #     forward = Forward().start(self.forward_to_fallback[0], self.forward_to_fallback[1])

        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as e:
            print("\t - Grott - grottproxy forward error : ", e) 
            #print(e)
            return False  

class Proxy:
    input_list = []
    channel = {}
    bHadServerContact = False
    lastServerContactTime = datetime.now()

    def __init__(self, conf):
        print("\nGrott proxy mode started")

        # for compatibility reasons test if libscrc is installed and send error message
        # if not installed processing wil continue but records will only be validated on length and not on crc. 
        try:     
            import libscrc
        except:
            print("\t **********************************************************************************")
            print("\t - Grott - libscrc not installed, no CRC checking only record validation on length!") 
            print("\t **********************************************************************************")

        ## to resolve errno 32: broken pipe issue (Linux only)
        if sys.platform != 'win32':
            signal(SIGPIPE, SIG_DFL) 
        ## 
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #set default grottip address
        if conf.grottip == "default" : conf.grottip = '0.0.0.0'
        self.server.bind((conf.grottip, conf.grottport))
        #socket.gethostbyname(socket.gethostname())
        try: 
            hostname = (socket.gethostname())    
            print("Hostname :", hostname)
            print("IP : ", socket.gethostbyname(hostname), ", port : ", conf.grottport, "\n")
        except:  
            print("IP and port information not available") 

        self.server.listen(200)
        self.forward_to = (conf.growattip, conf.growattport)
        # ! these fallback port ip and port options need to be moved to the config at some point
        self.forward_to_fallback = ("127.0.0.1", 5781)

        print("trying to connect to: " + str(self.forward_to) + " with fallback: "+ str(self.forward_to_fallback))

        self.isConnectedToGrowattTimer = threading.Timer(10, self.growattserverUnreachable)
        #print(self.forward_to)
        #print("fallback is:")
        #print(self.forward_to_fallback)
        
    def main(self,conf):
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            
            
            # if self.bHadServerContact:
            #     print((datetime.now()-self.lastServerContactTime).total_seconds())
            
            inputready, outputready, exceptready = ss(self.input_list, [], [])

            #print("checking remote server availability:")
            #self.checkServerAvailability()

            
            for self.s in inputready:
                         
            
                if self.s == self.server:
                    self.on_accept(conf)
                    break
                try: 
                    self.data, self.addr = self.s.recvfrom(buffer_size)
                except: 
                    if conf.verbose : print("\t - Grott connection error") 
                    self.on_close(conf)   
                    break
                if len(self.data) == 0:
                    self.on_close(conf)
                    break
                else:
                    self.on_recv(conf)

    def growattserverUnreachable(self):
        print("Growatt servers are unreachable!")
        #self.isConnectedToGrowattTimer.start()

    def checkServerAvailability(self):
        bAvailable = False
        if len(self.input_list)==3:
            print("remote server in input list")
            remoteServerSocket = self.input_list[2]
            print(remoteServerSocket)
            data = remoteServerSocket.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            print(len(data))
            print(data)
            
        else:
            print("input list too short")


        
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.settimeout(5)

        # try:
        #     bAvailable = (s.connect_ex(self.forward_to[0], self.forward_to[1])==0)
        #     if bAvailable:
        #         s.shutdown(socket.SHUT_RDWR)
        # except:
        #     bAvailable = False
        # s.close()

        return bAvailable

    def on_accept(self,conf):
        #print("checking remote availability...")
        #bAvailable = self.checkServerAvailability()
        #print("growatt remote server not available, falling back to local grott server")

        
        forward = Forward().start(self.forward_to[0], self.forward_to[1])
        if not forward:
            print("Growatt webservers are not responding, falling back to local grott server")
            forward = Forward().start(self.forward_to_fallback[0], self.forward_to_fallback[1])
        else:
            if self.isConnectedToGrowattTimer.is_alive():
                self.isConnectedToGrowattTimer.cancel()
            self.isConnectedToGrowattTimer.start()

        self.lastServerContactTime = datetime.now()
        clientsock, clientaddr = self.server.accept()

        if forward:
            #if conf.verbose: print("\t -", clientaddr, "has connected")
            print("\t -", clientaddr, "has connected")
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            if conf.verbose: 
                print("\t - Can't establish connection with remote server."),
                print("\t - Closing connection with client side", clientaddr)
            clientsock.close()

    def on_close(self,conf):
        if conf.verbose: 
            #try / except to resolve errno 107: Transport endpoint is not connected 
            try: 
                print("\t -", self.s.getpeername(), "has disconnected")
            except:  
                print("\t -", "peer has disconnected")

        #remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self,conf):
        data = self.data      
        #print("")
        #print("\t - " + "Growatt packet received:") 
        #print("\t\t ", self.channel[self.s])
        
        #test if record is not corrupted
        vdata = "".join("{:02x}".format(n) for n in data)
        validatecc = validate_record(vdata)
        if validatecc != 0 : 
            print(f"\t - Grott - grottproxy - Invalid data record received, processing stopped for this record")
            #Create response if needed? 
            #self.send_queuereg[qname].put(response)
            return  

        # FILTER!!!!!!!! Detect if configure data is sent!
        header = "".join("{:02x}".format(n) for n in data[0:8])
        if conf.blockcmd : 
            #standard everything is blocked!
            print("\t - " + "Growatt command block checking started") 
            blockflag = True 
            #partly block configure Shine commands                   
            if header[14:16] == "18" :         
                if conf.blockcmd : 
                    if header[6:8] == "05" or header[6:8] == "06" : confdata = decrypt(data) 
                    else :  confdata = data

                    #get conf command (location depends on record type), maybe later more flexibility is needed
                    if header[6:8] == "06" : confcmd = confdata[76:80]
                    else: confcmd = confdata[36:40]
                    
                    if header[14:16] == "18" : 
                        #do not block if configure time command of configure IP (if noipf flag set)
                        if conf.verbose : print("\t - Grott: Shine Configure command detected")                                                    
                        if confcmd == "001f" or (confcmd == "0011" and conf.noipf) : 
                            blockflag = False
                            if confcmd == "001f": confcmd = "Time"
                            if confcmd == "0011": confcmd = "Change IP"
                            if conf.verbose : print("\t - Grott: Configure command not blocked : ", confcmd)    
                    else : 
                        #All configure inverter commands will be blocked
                        if conf.verbose : print("\t - Grott: Inverter Configure command detected")
            
            #allow records: 
            if header[12:16] in conf.recwl : blockflag = False     

            if blockflag : 
                print("\t - Grott: Record blocked: ", header[12:16])
                if header[6:8] == "05" or header[6:8] == "06" : blockeddata = decrypt(data) 
                else :  blockeddata = data
                print(format_multi_line("\t\t ",blockeddata))
                return

        
        
        header = "".join("{:02x}".format(n) for n in data[0:8])
        rectype = header[14:16]
        

        if (self.s == self.input_list[2]):
            

            
            print("package from server")
            try:
                if (self.s.getpeername()[0] == socket.gethostbyname(self.forward_to[0])):
                    print("server is remote growatt server")
                    serverContactTime = datetime.now()
                    print("time since last contact with growatt server:")
                    timeSinceLastServerContact = (serverContactTime-self.lastServerContactTime).total_seconds()
                    print(timeSinceLastServerContact)
                    self.lastServerContactTime = serverContactTime
                    self.bHadServerContact = True
                #print(self.s.getpeername())
            except:
                print("server seems to be the local fallback server")
            #print(serverContactTime)
            

        elif(self.s == self.input_list[1]):
            print("package from datalogger")
    
        #print(header)
        #print(rectype)
        
        # if rectype in "04":
        #     print("data package from:")
        #     print(self.s.getpeername())
        
        #     print("content:")
        #     print(format_multi_line("\t\t ",data))

        # send data to destination
        self.channel[self.s].send(data)
        if len(data) > conf.minrecl :
            #process received data
            procdata(conf,data)    
        else:     
            if conf.verbose: print("\t - " + 'Data less then minimum record length, data not processed') 
                