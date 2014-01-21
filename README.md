Raspberry Pi Workshop: IP finder
===============================

Find your Raspberry Pi IP address once it is connected to Internet.

Consists of two parts:
 - _agent_

   Tiny go deamon that runs on the Raspberry Pi.
   To install on a device, from RaspberryPi do: 
   ```curl  http://raspberry-pi.seoultechsociety.org/get | sh```

 - _server_

   Available at http://raspberry-pi.seoultechsociety.org
   Show known devices, updates the list if a new one comes up.
