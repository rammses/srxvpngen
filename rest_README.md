## Enabling rest API

Srx devices come with a setting that enables some services accessible through internal interfaces,
as a security precaution, only standart/known ports are allowed through management enabled zones

As a result you can't access them directly. What do you need to do is delete the default setting as shown below 

    # delete security zones security-zone Internal host-inbound-traffic system-services all

and add new settings so all the services can be accessible
    
    # set security zones security-zone Internal host-inbound-traffic system-services any-service
    # commit

After this you can enable the rest api, since this is a test environment make sure you secure the access

    # set system services rest http port 3000
    # set system services rest enable-explorer

After this point you can access the rest api through 

    http://your_device_ip:3000