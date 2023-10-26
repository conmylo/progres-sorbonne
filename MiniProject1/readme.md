# Description of the project:

##### Nadir Shikhli - 21219384
##### Konstantinos Mylonas - 21306683

### Exercise 1: TCP Relay

This exercise is about creating a TCP relay
that stands between the server and the client.
There are 3 files: the server, the client 
and the relay.

### Exercise 2: HTTP Relay

This exercise is about modifying the TCP relay 
into an HTTP relay. Instead of a web browser 
as the client, we use the client.py file, which 
emulates a web request and gives us the 
results we need. The server file contains the 
functions responsible for initializing the server
and handling the connection with the relay.

This exercise has 4 parts. Every part is in a
different folder. The server and client files are
the same in every folder. The only difference is 
the port numbers in the chain folder, since we 
need to chain the server, the client and the
3 relays to each other.

In the chain 
folder, the client is first sending the message to 
the censor relay. Then the censor relay is connected to the cache relay, the cache relay is connected to the
logger relay and finally that is connected to our server.
In order to test it, one has first to run the server,
then the relays: logger, cache, censor and finally the
client. 

