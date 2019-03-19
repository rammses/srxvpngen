# srxvpngen
Creates vpn tunnels in srx devices using netconf


## Dependency installations for PYez modules

		#sudo apt install  python3-pip python3-dev libxml2-dev libxslt-dev libssl-dev libffi-dev

##Updating the PIP3 repositories
		#pip3 install --upgrade pip

## Installation of PYez

		#pip3 install junos-eznc

## Creating a keypair and a Netconf user to establish connection using PYez 
## Server side steps 
do not use passwords in keypair

		# ssh-keygen -t rsa
		Generating public/private rsa key pair.
		Enter file in which to save the key (/root/.ssh/id_rsa): srxvpngen_nopass
		Enter passphrase (empty for no passphrase):
		Enter same passphrase again:
		Your identification has been saved in tsrxvpngen_nopass.
		Your public key has been saved in srxvpngen_nopass.pub.
		The key fingerprint is:
		SHA256:39dwxZTgeRK4T+p6T5eKL3hgDv1tTtb8ZB81T7bGT8o root@ubuntu
		The key's randomart image is:
		+---[RSA 2048]----+
		|            .o. o|
		|           .. o+ |
		|            .+ .o|
		|           . .o .|
		|        S   + ..=|
		|       . = o .+**|
		|        + * o+.X*|
		|         o *==+==|
		|         .+.*=E +|
		+----[SHA256]-----+


1. this command creates 2 files, one has a pub extension. You need upload this file to /var/tmp folder on remote device 
and add it to users authentication method and example is show below switch side steps
2. The private key file must be used as identity file while creating a connection to junos device 

put the public key file using scp to switch


		# scp srxvpngen_nopass.pub root@192.168.17.130:/var/tmp/srxvpngen_nopass.pub
		Password:

## SRX side steps
### Creating a Superuser enabled user with key only authentication 

-----------
		{master:0}[edit]
		root@SWH_PS_WS_CA0201# set system login user srxvpngen class super-user authentication load-key-file /var/tmp/srxvpngen_nopass.pub                                                                                                               ^
		#commit
-----------

### Enable netconf with port change def=830

		root@SWH_PS_WS_CA0201# set system services netconf ssh
		{master:0}[edit]
		root@SWH_PS_WS_CA0201# show | compare
		[edit system services]
		+    netconf {
		+        ssh;
		+    }
		{master:0}[edit]
		root@SWH_PS_WS_CA0201# commit
		configuration check succeeds
		commit complete

## Testing

If you receive what we call dev.hello as shown below everything is fine. You've established an PYez connection to junos switch
	
	PS C:\Python_Calisma\srxvpngen\keys> ssh -i .\srxvpngen_nopass srxvpngen@192.168.17.130 -p 830 -s netconf
    <!-- No zombies were killed during the creation of this user interface -->
    <!-- user srxvpngen, class j-super-user -->
    <hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <capabilities>
        <capability>urn:ietf:params:netconf:base:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:candidate:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:confirmed-commit:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:validate:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:url:1.0?scheme=http,ftp,file</capability>
        <capability>urn:ietf:params:xml:ns:netconf:base:1.0</capability>
        <capability>urn:ietf:params:xml:ns:netconf:capability:candidate:1.0</capability>
        <capability>urn:ietf:params:xml:ns:netconf:capability:confirmed-commit:1.0</capability>
        <capability>urn:ietf:params:xml:ns:netconf:capability:validate:1.0</capability>
        <capability>urn:ietf:params:xml:ns:netconf:capability:url:1.0?protocol=http,ftp,file</capability>
        <capability>http://xml.juniper.net/netconf/junos/1.0</capability>
        <capability>http://xml.juniper.net/dmi/system/1.0</capability>
      </capabilities>
      <session-id>5222</session-id>
    </hello>
    ]]>]]>


##Using the srxvpn.py
It has 3 switches
### Create
It takes 6 paramaters as explained below
                                                                                               
     #python srxvpngen.py -C test243 ge-0/0/0 123.123.123.123 192.168.17.0/24 192.168.36.0/24 135 
                           | |       |        |               |               |               |   
                           | |       |        |               |               |               ---- Tunnel Number
                           | |       |        |               |               -------------------- Destination Network
                           | |       |        |               ------------------------------------ Source Network
                           | |       |        ---------------------------------------------------- Destination endpoint
                           | |       ------------------------------------------------------------- Source interface
                           | --------------------------------------------------------------------- Tunnel Name
                           ----------------------------------------------------------------------- create switch
    
### List
It takes no parameters just shows configured vpn tunnels

### Delete
It takes one parameter 
    python srxvpngen.py -D tunnel_name
