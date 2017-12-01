#Python 3.6
#Made to run on Windows at command prompt
#the main function runs it all and calls the other functions


from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
#import pandas as pd
import getpass
import os

platform = 'cisco_ios'
fopen = open('ips.txt', 'r')
hosts = fopen.read().splitlines()
_username = raw_input('Enter your username: ')
password = getpass.getpass('Password: ')
#_username = ''
#password = ''

mac_list=[]


#Define functions below

def main():
    for i in hosts:
        net_connect = connect_to_host(i) #connect to host
        #get hostname
        hostname = getHostname(net_connect)
        print(hostname)
        #open a file to write mac addresses to ;this should be a database later
        int_list = get_interfaces(net_connect) #get the list of interfaces, read into list
        #feed the list of interfaces into another loop that gets the mac address of each & &
        for x in int_list:
            _a = get_mac(net_connect, x)
            _a.insert(0,x)
            mac_list.append(_a)
        #write the macs to a temp file, ex: hostname_temp.csv
        write_file(mac_list, hostname)
        #compare the contents of the temp file to the previous version of the mac_address file
        check_macs(hostname)
        #alert on any changes to the mac file
        #rename the old mac file and make this mac address file the new one to be compared to next time
        #print(mac_list)
        print(str(i) + ' done')

def check_macs(name):
    f_temp = name + '_temp.csv'
    f_name_old = name + '.csv'
    with open(f_name_old, 'rb') as csvfile1:
        with open (f_temp, "rb") as csvfile2:
            #open the csv files and read them into lists
            reader1 = csv.reader(csvfile1)
            content1 = list(reader1)
            reader2 = csv.reader(csvfile2)
            content2 = list(reader2)
            #run a loop and compare the two lists
            file_length = len(content1)
            ctr = 0
            while ctr < file_length:
                #read the values in the content files
                _a = content1[ctr]
                _b = content2[ctr]
                #loop through the files and compare the lists
                max = len(_a)
                _ctr1 = 0
                while _ctr1 < max:
                    #make sure that the two values are not null(ie nothing in the ports on both)
                    if _a[_ctr1] != '' or _b[_ctr1] != '':
                        if _a[_ctr1] != _b[_ctr1]:
                            write_results(_a, _b, name)
                    _ctr1 += 1
                ctr+=1

def getHostname(net_connect):
    host = net_connect.find_prompt()
    return host.replace("#",'')

def write_file(list, name):
    file_name = name + '_temp.csv'
    my_df = pd.DataFrame(list)
    my_df.to_csv(file_name, index=False, header=False)


def write_results(a, b, name):
    with open('scan_results.txt', 'a')as out_file:
        out_file.write('Scan results for ' + name + '\n')
        out_file.write(str(a)+ '\n')
        out_file.write(str(b)+ '\n')
        out_file.write('*'*100 + '\n')


def get_mac(connect, interface_name):
    c_command = 'sh mac address-table ' + str(interface_name) + ' | include dynamic'
    raw_output = connect.send_command(c_command)
    #extract the macs
    output_lines = raw_output.split('\n')
    out_list = []
    for x in output_lines:
        line_split = x.split()
        if len(line_split) == 5:
            vlan, mac_addr, type, protocols, port = line_split
            out_list.append(mac_addr)
        elif len(line_split) == 4:
            vlan, mac_addr, type, port = line_split
            out_list.append(mac_addr)
    return out_list


def get_interfaces(net_connect):
    #get the interfaces
    output_gig = net_connect.send_command('sh run | inc interface Gigabit')
    output_fast = net_connect.send_command('sh run | inc interface Fast')
    #output_tengig = net_connect.send_command('sh run | inc interface TenGigabit')
    #put them in a usable list
    make_list_fast = make_list(output_fast)
    make_list_gig = make_list(output_gig)
    #combine them into a MEGALIST!
    int_list = make_list_fast + make_list_gig
    return int_list

def connect_to_host(_ip):
    try :
        return ConnectHandler(device_type=platform, username=_username,ip=_ip, password=password)
    except(NetMikoTimeoutException):
        print (str(i) + ' is not reachable')
    except(NetMikoAuthenticationException):
        print (' Cannot connect . . . bad username or password')


def make_list(input):
    f_out = open('ethernet.txt', 'w')
    f_out.write(input)
    f_out.close()
    f_in = open('ethernet.txt', 'r+')
    raw_data = f_in.readlines()
    f_in.close()
    #clean up the data and remove blank lines
    data = [s.rstrip() for s in raw_data]
    return data



main()





#########################OLD CODE######################################################

##def get_interfaces(net_connect):
##    print('getint ran')
##    output = net_connect.send_command('sh run | inc interface Gigabit')
##    output_two = net_connect.send_command('sh run | inc interface Fast')
##    output_three = net_connect.send_command('sh run | inc interface TenGigabit')
##    print (output)
##    print (output_two)
##    f_out = open('ethernet.txt', 'a')
##    f_out.write(output)
##    f_out.write('\n')
##    f_out.write(output_two)
##    f_out.close()
##    #print('getint done')
##    #pass
##    net_connect.disconnect()

    #run your commands
##    print('*' * 100)
##    print ('Connecting to. . . . ' + str(i))
##    hostname = net_connect.find_prompt()
##    hostname = hostname.replace("#",'')
##    print('-' * 100)
##    print (hostname)

    
    #output = net_connect.send_command('sh run | inc hostname')
    #print (output)
    #print (output_two)
##    output = net_connect.send_command('sh mac address-table')
##    #break the output into lines split on newline character
##    output_lines = output.split('\n')
##    output_list = []
##    #iterate through and put into list
##    for x in output_lines:
##        line_split = x.split()
##        if len(line_split) == 5:
##            vlan, mac_addr, type, protocols, port = line_split
##            output_list.append((port, mac_addr))
##        elif len(line_split) == 4:
##            vlan, mac_addr, type, port = line_split
##            output_list.append((port, mac_addr))
##    for i in output_list:
##        print (i)
##    #pprint.pprint(output_list)   
    #print (output)
    #print('*' * 100)
    
##        for i in int_list:
##            print(i)
#print('all done')
