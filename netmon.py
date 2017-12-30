#Python 3.6
#Made to run on Windows at command prompt
#the main function runs it all and calls the other functions

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
import time
import datetime
import getpass
import os

platform = 'cisco_ios'
fopen = open('ips.txt', 'r')
hosts = fopen.read().splitlines()
_username = raw_input('Enter your username: ')
password = getpass.getpass('Password: ')
#_username = ''
#password = ''
hosts_checked = []
current_mac_list=[]

#Define functions below

def main():
    for i in hosts:
        net_connect = connect_to_host(i) #connect to host
        print('connected')
        #get hostname
        hostname = getHostname(net_connect)
        #be sure we havent previously checked this hostname
        if hostname in hosts_checked:
            print('Duplicate host entry')
            continue
        print(hostname)
        #open a file to write mac addresses to ;this should be a database later
        int_list = get_interfaces(net_connect) #get the list of interfaces, read into list
        print('got int list')
        #feed the list of interfaces into another loop that gets the mac address of each & &
        current_mac_list = get_macs(net_connect, int_list)
        print('got macs')
        #compare the macs to see if any have never been seen before
        new_macs = check_macs(current_mac_list, hostname, net_connect)
        #add hostname to list of files checked
        hosts_checked.append(hostname)
        #print(mac_list)
        print(str(i) + ' done')


def check_macs(mac_list, host, connect):
    file_name = 'data_files/' + host + '.dat'
    if os.path.isfile(file_name):
        #the file exists so
        with open(file_name, 'a+') as mac_file:
            old_macs_list = mac_file.read().splitlines()
        for mac in mac_list:
            if mac not in old_macs_list:
                write_results(mac, host, connect)
                old_macs_list.append(mac)
                #mac_file.write(mac)
        with open(file_name, 'w+') as out_file:
            for m in old_macs_list:
                out_file.write(m + '\n')
    else:
        print('File not present for {}, probably a new device' .format(host))
        write_file(mac_list, host)

def get_port(mac, host, connect):
    c_command = 'show mac address-table address ' + mac
    raw_output = connect.send_command(c_command)
    return raw_output


def getHostname(net_connect):
    host = net_connect.find_prompt()
    return host.replace("#",'')

def write_file(list, name):
    #os.chdir('data_files')
    file_name = 'data_files/' + name + '.dat'
    with open(file_name, 'a') as out_file:
        for i  in list:
            out_file.write(i + '\n')

def write_results(mac, name, connect):
    with open('scan_results.txt', 'a')as out_file:
        d = time.strftime("%Y-%m-%d %H:%M")
        out_file.write('Scan results for ' + name +  ' at ' +  str(d) + '\n')
        out_file.write('This mac has not been seen before:   ' + str(mac)+ '\n')
        command_output = get_port(mac, name, connect)
        out_file.write(command_output + '\n')
        out_file.write('MAC added to the list so this message will not show again' + '\n')
        out_file.write('*'*100 + '\n')


def get_macs(connect, int_list):
    out_list = []
    for interface in int_list:
        c_command = 'sh mac address-table ' + str(interface) + ' | include dynamic'
        raw_output = connect.send_command(c_command)
        #extract the macs
        output_lines = raw_output.split('\n')
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
    #put all interfaces into a list
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
    #writing it to a file to remove the u\ that preceds the output - need to find a more effiecent way to do this
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



