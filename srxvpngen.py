#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Junos Vpn generator
- Generates vpn tunnels based on config.yml
- lists tunnels
- deletes tunnel
"""
__author__ = "Mesut Bayrak 'Rammses' "
__copyright__ = "Copyright 2016, ISTANBUL"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mesut Bayrak"
__email__ = "mesut@mikronet.net"
__status__ = "Beta "

import sys, os,datetime,threading, requests, csv, yaml, time, argparse, secrets, string, paramiko, time, logging, yaml, datetime
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

def config_data():
    with open('./config.yml', 'r') as ymlfile:
        config_data = yaml.load(ymlfile)
    return config_data

def ListTunnels(_host,_port,_username,_password,_command):
    return

def send_commands(_hostname, _port, _username, _keyfile,_commands):
    dev = Device(host=_hostname, port=_port,user=_username,
                 ssh_private_key_file=_keyfile).open()
    with Config(dev, mode='private') as cu:
        try:
            print('Uploading config')
            x=0
            for i in _commands:
                print(len(_commands))
                print(_commands[x])
                cu.load(_commands[x], format='set')
                x+=1
            print('done')
            print('receiving diff output')
            cu.pdiff()
            before_commit = datetime.datetime.now()
            print('executing commit\n', before_commit)
            cu.commit()
            after_commit = datetime.datetime.now()
            print('done\n', after_commit)
            delta_time = after_commit - before_commit
            print(delta_time)
            _success = True
            return _success
        except:
            _success = False
            return _success

def generatedpsk(secret_length):
    stringSource = string.ascii_letters + string.digits \
                   # + string.punctuation
    password = secrets.choice(string.ascii_lowercase)
    password += secrets.choice(string.ascii_uppercase)
    password += secrets.choice(string.digits)
    # password += secrets.choice(string.punctuation)
    for i in range(secret_length):
        password += secrets.choice(stringSource)
    char_list = list(password)
    secrets.SystemRandom().shuffle(char_list)
    password = ''.join(char_list)
    return password

def main():

    # Read config data from yml
    config = config_data()

    # ArgParse case operations
    parser = argparse.ArgumentParser(description='Creates vpn tunnels')
    parser.add_argument('-C','--create',
                    nargs='+',
                    required=False,
                    help='vpn tunnel creator requires 5 parameters name, interfece,remote gatewayip, source net, destination net')
    parser.add_argument('-D','--delete',
                    required=False,
                    help='tunnel delete requires 1 paramaeter which is the name of tunnel')
    parser.add_argument('-L','--list',
                    required=False,
                    action='store_true',
                    help='lists vpn tunnels requires no parameter --detail shows tunnel status')
    parser.add_argument('-V','--verbose',
                    required=False,
                    help='Start verbose logging to stdout')
    args = parser.parse_args()

    if args.create:

        # Read credential config
        _firewall = config['credentials']['firewall']
        _fwport = config['credentials']['port']
        _fwuser = config['credentials']['user']
        _fwpass = config['credentials']['pass']
        _fwkeyfile = config['credentials']['keyfile']



        # parameters from create
        _tunnelname = args.create[0]
        _tunnelint = args.create[1]
        _tunneldest = args.create[2]
        _tunnellocal = args.create[3]
        _tunnelremote = args.create[4]
        _tunnelnumber = args.create[5]

        # parameters from create switch simulated
        # _tunnelname = 'tunnel_1'
        # _tunnelint = 'ge-0/0/0'
        # _tunneldest = '101.101.101.102'
        # _tunnellocal = '192.168.17.0/24'
        # _tunnelremote = '172.16.37.0/24'
        # _tunnelnumber = '124'

        # conversion and additions to parameters
        _tunnellocal_AB = _tunnellocal.replace('.', '_')
        _tunnelremote_AB = _tunnelremote.replace('.', '_')
        _tunnellocal_ABEnt = "_addr_" + _tunnellocal_AB.replace('/', '_') + " "
        _tunnelremote_ABEnt = "_addr_" + _tunnelremote_AB.replace('/', '_') + " "

        _key_length = int(config['Ike-Policy']['Key-Len'])

        # construct vpn tunnel config script.

        Model4 = ['set security ike policy ike_pol_' + _tunnelname + ' mode ' + config['Ike-Policy']['mode']], \
                 ['set security ike policy ike_pol_' + _tunnelname + ' proposal-set ' + config['Ike-Policy']['prop-set']], \
                 ['set security ike policy ike_pol_' + _tunnelname + ' pre-shared-key ascii-text ' + '\'' +generatedpsk(_key_length) + '\''], \
                 ['set security ike gateway gw_' + _tunnelname + ' ike-policy ike_pol_' + _tunnelname], \
                 ['set security ike gateway gw_' + _tunnelname + ' address ' + _tunneldest], \
                 ['set security ike gateway gw_' + _tunnelname + ' dead-peer-detection'], \
                 ['set security ike gateway gw_' + _tunnelname + " external-interface " + _tunnelint], \
                 ['set security ipsec policy ipsec_pol_' + _tunnelname + ' perfect-forward-secrecy ' +config['Ipsec-pol']['pfs']], \
                 ['set security ipsec policy ipsec_pol_' + _tunnelname + ' proposal-set ' + config['Ipsec-pol']['prop-set']], \
                 ['set security ipsec vpn ' + _tunnelname + ' bind-interface st0.' + _tunnelnumber], \
                 ['set security ipsec vpn ' + _tunnelname + ' vpn-monitor'], \
                 ['set security ipsec vpn ' + _tunnelname + ' ike gateway gw_' + _tunnelname], \
                 ['set security ipsec vpn ' + _tunnelname + ' ike ipsec-policy ipsec_pol_' + _tunnelname], \
                 ['set security ipsec vpn ' + _tunnelname + ' establish-tunnels immediately'], \
                 ['set security zones security-zone ' + config['Firewall']['zone'] + ' address-book address ' + _tunnelname + _tunnellocal_ABEnt + _tunnellocal], \
                 ['set security zones security-zone ' + config['Firewall']['zone'] + ' address-book address ' + _tunnelname + _tunnelremote_ABEnt + _tunnelremote], \
                 ['set security policies from-zone ' + config['Firewall']['zone'] + ' to-zone ' + config['Firewall']['zone'] + ' policy policy_out_' + _tunnelname + ' match source-address ' + _tunnelname + _tunnellocal_ABEnt], \
                 ['set security policies from-zone ' + config['Firewall']['zone'] + ' to-zone ' + config['Firewall']['zone'] + ' policy policy_out_' + _tunnelname + ' match destination-address ' + _tunnelname + _tunnelremote_ABEnt], \
                 ['set security policies from-zone ' + config['Firewall']['zone'] + ' to-zone ' + config['Firewall']['zone'] + ' policy policy_out_' + _tunnelname + ' match application any'], \
                 ['set security policies from-zone ' + config['Firewall']['zone'] + ' to-zone ' + config['Firewall']['zone'] + ' policy policy_out_' + _tunnelname + ' then permit'], \
                 ['set security policies from-zone ' + config['Firewall']['zone'] + ' to-zone ' + config['Firewall']['zone'] + ' policy policy_in_' + _tunnelname + ' match source-address ' + _tunnelname + _tunnelremote_ABEnt], \
                 ['set security policies from-zone ' + config['Firewall']['zone'] + ' to-zone ' + config['Firewall']['zone'] + ' policy policy_in_' + _tunnelname + ' match destination-address ' + _tunnelname + _tunnellocal_ABEnt], \
                 ['set security policies from-zone ' + config['Firewall']['zone'] + ' to-zone ' + config['Firewall']['zone'] + ' policy policy_in_' + _tunnelname + ' match application any'], \
                 ['set security policies from-zone ' + config['Firewall']['zone'] + ' to-zone ' + config['Firewall']['zone'] + ' policy policy_in_' + _tunnelname + ' then permit'], \
                 ['set security zones security-zone ' + config['Firewall']['zone'] + ' interfaces st0.' + _tunnelnumber], \
                 ['set interfaces st0 unit ' + _tunnelnumber + ' family inet '], \
                 ['set routing-options static route ' + _tunneldest + ' next-hop st0.' + _tunnelnumber]

        #Cleari brackets and join members to 1 list
        counter1 = 0
        _data = []
        for i in Model4:
            for y in i:
                # print(counter1, Model4[counter1])
                _data.append(y)
        print(_data)

        #sending commands
        # _command = ['set system host-name "changed_to_test2"', 'set system host-name "changed_to_test3"']
        send_commands(_firewall, _fwport,_fwuser,_fwkeyfile, _data)


    elif args.delete:
        print("delete")
        _del_tunnelname = args.delete[0]
        # Read credential config
        _firewall = config['Credentials']['firewall']
        _fwport = config['Credentials']['port']
        _fwuser = config['Credentials']['user']
        _fwpass = config['Credentials']['pass']
        delete_tunnels = ListTunnels(_firewall, _fwport, _fwuser, _fwpass, _Script_Delete_Tunnel)
        print(_firewall, _fwport, _fwuser, _fwpass, _Script_Delete_Tunnel)
        print(delete_tunnels)

    elif args.list:
        # Read credential config
        _firewall = config['Credentials']['firewall']
        _fwport = config['Credentials']['port']
        _fwuser = config['Credentials']['user']
        _fwpass = config['Credentials']['pass']
        get_tunnels = ListTunnels(_firewall, _fwport, _fwuser, _fwpass, _Script_Get_Tunnels)
        # print(_firewall, _fwport, _fwuser, _fwpass, _Script_Get_Tunnels)
        print(*get_tunnels, sep='\n')

if __name__ == "__main__":
    main()



