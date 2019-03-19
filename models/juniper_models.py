# from srxvpngen import _tunnelname as _tunnelname
from __main__ import _tunnellocal
# import yaml, string, secrets
#
#
# def config_data():
#     with open('C:/Users/rammses/ownCloud/Python_Calisma/srxvpngen/config.yml', 'r') as ymlfile:
#         config_data = yaml.load(ymlfile)
#     return config_data
# def generatedpsk(secret_length):
#     stringSource = string.ascii_letters + string.digits + string.punctuation
#     password = secrets.choice(string.ascii_lowercase)
#     password += secrets.choice(string.ascii_uppercase)
#     password += secrets.choice(string.digits)
#     password += secrets.choice(string.punctuation)
#     for i in range(secret_length):
#         password += secrets.choice(stringSource)
#     char_list = list(password)
#     secrets.SystemRandom().shuffle(char_list)
#     password = ''.join(char_list)
#     return password
#
# #Read config data from yml
# config = config_data()



# parameters from create
# _tunnelname = args.create[0]
# _tunnelint = args.create[1]
# _tunneldest = args.create[2]
# _tunnellocal = args.create[3]
# _tunnelremote = args.create[4]
# _tunnelnumber = args.create[5]

# parameters from create switch simulated
# _tunnelname = 'tunnel_1'
# _tunnelint = 'ge-0/0/0'
# _tunneldest = '101.101.101.102'
# _tunnellocal = '192.168.17.0/24'
# _tunnelremote = '172.16.37.0/24'
# _tunnelnumber = '124'

#conversion and additions to parameters
# _key_length=int(config['Ike-Policy']['Key-Len'])
_tunnellocal_AB = _tunnellocal.replace('.','_')
_tunnelremote_AB = _tunnelremote.replace('.','_')
_tunnellocal_ABEnt= "_addr_" +_tunnellocal_AB.replace('/','_')+" "
_tunnelremote_ABEnt= "_addr_" +_tunnelremote_AB.replace('/','_')+" "


Model4=['set security ike policy ike_pol_' + _tunnelname +' mode ' + config['Ike-Policy']['mode']],\
       ['set security ike policy ike_pol_' + _tunnelname +' proposal-set ' + config['Ike-Policy']['prop-set']],\
       ['set security ike policy ike_pol_' + _tunnelname +' pre-shared-key ' + generatedpsk(_key_length)],\
       ['set security ike gateway gw_' + _tunnelname +' ike-policy ike_pol_' + _tunnelname ],\
       ['set security ike gateway gw_' + _tunnelname +' address '+ _tunneldest ],\
       ['set security ike gateway gw_' + _tunnelname + ' dead-peer-detection'],\
       ['set security ike gateway gw_' + _tunnelname +" external-interface "+ _tunnelint ],\
       ['set security ipsec policy ipsec_pol_' + _tunnelname +' perfect-forward-secrecy '+ config['Ipsec-pol']['pfs']],\
       ['set security ipsec policy ipsec_pol_' + _tunnelname +' proposal-set'+ config['Ipsec-pol']['prop-set']],\
       ['set security ipsec vpn ' + _tunnelname +' bind-interface st0.'+_tunnelnumber],\
       ['set security ipsec vpn ' + _tunnelname +' vpn-monitor'],\
       ['set security ipsec vpn ' + _tunnelname +' ike gateway gw_' + _tunnelname ],\
       ['set security ipsec vpn ' + _tunnelname +' ike ipsec-policy ipsec_pol_' + _tunnelname ],\
       ['set security ipsec vpn ' + _tunnelname +' establish-tunnels immediately'],\
       ['set security zones security-zone ' + config['Firewall']['zone'] +' address-book address ' + _tunnelname + _tunnellocal_ABEnt + _tunnellocal],\
       ['set security zones security-zone ' + config['Firewall']['zone'] +' address-book address ' + _tunnelname + _tunnelremote_ABEnt+ _tunnelremote ],\
       ['set security policies from-zone ' + config['Firewall']['zone'] +' to-zone ' + config['Firewall']['zone'] +' policy policy_out_' + _tunnelname +' match source-address ' + _tunnelname + _tunnellocal_ABEnt],\
       ['set security policies from-zone ' + config['Firewall']['zone'] +' to-zone ' + config['Firewall']['zone'] +' policy policy_out_' + _tunnelname +' match destination-address ' + _tunnelname + _tunnelremote_ABEnt],\
       ['set security policies from-zone ' + config['Firewall']['zone'] +' to-zone ' + config['Firewall']['zone'] +' policy policy_out_' + _tunnelname +' match application any'],\
       ['set security policies from-zone ' + config['Firewall']['zone'] +' to-zone ' + config['Firewall']['zone'] +' policy policy_out_' + _tunnelname +' then permit'],\
       ['set security policies from-zone ' + config['Firewall']['zone'] +' to-zone ' + config['Firewall']['zone'] +' policy policy_in_' + _tunnelname +' match source-address ' + _tunnelname + _tunnelremote_ABEnt],\
       ['set security policies from-zone ' + config['Firewall']['zone'] +' to-zone ' + config['Firewall']['zone'] +' policy policy_in_' + _tunnelname +' match destination-address ' + _tunnelname +_tunnellocal_ABEnt],\
       ['set security policies from-zone ' + config['Firewall']['zone'] +' to-zone ' + config['Firewall']['zone'] +' policy policy_in_' + _tunnelname +' match application any'],\
       ['set security policies from-zone ' + config['Firewall']['zone'] +' to-zone ' + config['Firewall']['zone'] +' policy policy_in_' + _tunnelname +' then permit'],\
       ['set security zones security-zone ' + config['Firewall']['zone'] +' interfaces st0.'+_tunnelnumber],\
       ['set interfaces st0 unit '+_tunnelnumber+' family inet '],\
       ['set routing-options static route '+_tunneldest+' next-hop st0.'+_tunnelnumber]

# if __name__ == "__main__":
#     x = 0
#     for i in Model4:
#         print(x, Model4[x])
#         x += 1
