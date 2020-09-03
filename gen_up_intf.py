#!/usr/bin/env python3

'''
This script finds the interfaces that are in UP state.
This will create two files.
one for Physical interface called up_ethernet.yaml
second for Port channels called up_portchannel.yaml
Python napalm module is used to get interface details.
'''

import logging
import secrets
import argparse
import yaml
from napalm import get_network_driver

parser = argparse.ArgumentParser()
parser.add_argument('--switch_ip')
parser.add_argument('--switch_os', default='nxos_ssh', choices=['ios', 'nxos_ssh'])
args = parser.parse_args()

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(filename='logging.log', level=logging.INFO, format=FORMAT)

def main(switch_ip, switch_os):
    ''' main function '''
    f1 = open('up_ethernet.yaml', 'w')
    f2 = open('up_portchannel.yaml', 'w')
    driver = get_network_driver(switch_os)
    device = driver(switch_ip, secrets.sw_user, secrets.sw_pwd)
    device.open()

    # device.get_interfaces returns a dictionary
    # The interface names are keys of the dictionary
    # The values are another dictionary showing following info
    #   descrition
    #   is_enabled
    #   is_up
    #   last_flapped
    #   mac_address
    #   speed
    interface_list = device.get_interfaces()
    logging.debug(interface_list)
    device.close()

    up_ethernet = {}
    up_portchannel = {}

    # We are interested in Ethernet and Port-Channel interfaces in UP state.
    # We will exclude interfaces like vlan and mgmt0

    for interface, details in interface_list.items():
        if 'Ethernet' in interface and details['is_up']:
            up_ethernet[interface] = details
        if 'ort-channel' in interface and details['is_up']:
            up_portchannel[interface] = details
    
    print('** INFO: Number of Ethernet interfaces in UP state: {}'.format(len(up_ethernet)))
    print('** INFO: Number of Port Channels in UP state: {}'.format(len(up_portchannel)))
    print('Convert python dictionaries to yaml data')
    up_ethernet_yaml = yaml.dump(up_ethernet)
    up_portchannel_yaml = yaml.dump(up_portchannel)

    print('Write yaml data to files.')
    f1.write(up_ethernet_yaml)
    f2.write(up_portchannel_yaml)
    f1.close()
    f2.close()

if __name__ == "__main__":
    main(args.switch_ip, args.switch_os)