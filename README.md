# network-monitoring
This is a simple script built with Python and Netmiko that will poll a list of switches, make a list of connected MAC addresses, and check that list against the last time the script was run


Still a work in progress, need to now be able to add functions to alert for a change, delete the old mac file if there is an alert found or delete the tmep file, maybe a nice output file as well.

The MACs are stored into text files which is less than ideal so adding another type of storage would be beneficial.

Wish List:
Output to a html file or web framework 
Be able to execute pthon network commands from a web page
Full dashboard with site ids and mac addreesses
Ability to search across all devices for a particular mac
Alert at the presence of a particular MAC
