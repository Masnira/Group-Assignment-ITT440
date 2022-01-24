#server side
import socket #for socket
import os #to interact with operating system
import sys
import random 
import errno 
import math #to do math calculation
import datetime #get time for timestamp 
from multiprocessing import Process #parallel process

unicode = "utf-8" #Unicode Transformation Format
bufferSize = 2048 #buffer size

def process_start(s_sock):

    totalAns = 0 #totalAns declaration
    s_sock.send(str.encode('[Server]Kitchen Connected To The Cashier\t\t\t')) #send message to client if the socket connected
    
    while True:
        data = s_sock.recv(bufferSize) #receive from client
        data = data.decode(unicode) #encoding data to original data
        #print (data)
        
        #process/calculation
        try:
            food, num , value = data.split(":")
            opt = str(food)
            qty = int(num)
            prc = float(value)

            if opt[0]  == 'A':
                opt = 'Red Velvet Cake'
                prc = 20
                ans = qty * (prc)

            elif opt[0] == 'B':
                opt = 'Chicken Dumpling'
                prc = 15
                ans = qty * (prc)

            elif opt[0] == 'C':
                opt = 'Chicken Lasagna'
                prc = 10
                ans = qty * (prc)

            elif opt[0] == 'D':
                opt = 'Mineral Water'
                prc = 1
                ans = qty * (prc)

            elif opt[0] == 'E':
                opt = 'Soft Drinks'
                prc = 50
                ans = qty * (prc)

            elif opt[0] == 'F':
                opt = 'Cappucino'
                prc = 45
                ans = qty * (prc)

            elif opt[0] == 'G':
                opt = 'Smoothies'
                prc = 5
                ans = qty * (prc)

            else:
                ans = ('ERROR')
             
            
            calculate = (str(opt)+ '.... RM'+ str(prc)+ '['+ str(qty) + ']: RM' + str(ans))
            totalAns = totalAns + ans #calculate totalAns
            sendClient = ans #sendClient declare
            toClient = str(opt) #toClientDeclare
            print ('\n--Hi Kitchen--\n')
            print ('New Order Received!! ')
            
            print(calculate)
            totl = (str(opt)+ '.... '+ '|'+ str(qty))
            

            #open and write data to file
            file = open(r'total.txt', 'r')
            file = open(r'total.txt', 'w')
            file.write('Receipt Record \n')
            file.close

            file3 = open(r'total.txt', 'r')
            file3 = open(r'total.txt', 'a')  
            write3 = '\n' + calculate + '\n'
            file3.write(write3)
            file3.close

            file1 = open(r'quantity.txt', 'r')
            file1 = open(r'quantity.txt', 'w')
            file1.write('Total order Record \n')
            file1.close
        
            file2 = open(r'quantity.txt', 'r')
            file2 = open(r'quantity.txt', 'a')  
            write2 = '\n' + totl + '\n'
            file2.write(write2)
            file2.close

            

        except:
            print ("Connection Terminated From Client \n")
            #print ("Total Sales For :"  + str(s_addr))
            #print (totalAns)
            
            break

        if not data:
            break

        s_sock.send(str.encode(str(sendClient))) #send SendClient data to client (price)
        s_sock.send(str.encode(str(toClient))) #send toClient data to client (food)

        #print (sendClient)
        #print (toClient)
        jenis = s_sock.recv(bufferSize) #get data from server
        jenis = jenis.decode(unicode)
        #print(jenis)
        nombor = s_sock.recv(bufferSize) #get data from server
        nombor = nombor.decode(unicode)
        s_sock.send(str.encode(str(totalAns))) #send toClient data to client (food)

        #get type option
        if jenis[0]  == 'A':
           print("Take Away")
           

        elif jenis[0] == 'B':
           print("Dine in")   
           print("Table No:"+ str(nombor))

        else :
           print("Wrong Input!")     

        pid = os.fork() #fork
        
        if pid > 0 :
        
          print("Cashier ID:", os.getpid())
          
        else :
        
          break
        
    s_sock.close()

if __name__ == '__main__':
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",8888)) #port to bind
        print("[*] Listening from cashier...")
        s.listen(3) # 3 incoming connection to queue
        # get current time
        ct = datetime.datetime.now()
        try:
                while True:
                        try:
                                s_sock, s_addr = s.accept()
                                print('[*] Get data from : ' + str(s_addr))
                                print("current time:-", ct)
                                p = Process(target=process_start, args=(s_sock,))
                                p.start()

                        except socket.error:
                                print('Socket Error Problem!')

        except Exception as e:
                print("[*] An exception occured! ")
                print(e)
                sys.exit(1)
        finally:
                s.close()    
