Introduction:
--
This is the 2nd mini project for the PROGRES course of Sorbonne Universite 2023-2024 winter semester.

It is implemented in 3 files:
main.py: contains all the functions and routes of the API,
server.py: contains functions, templates and routes of the server,
tests.py: contains some unit tests to test the API.

Bibliography
--
StackOverflow was used to understand how to handle errors and exceptions.
ChatGPT 3.5 was used to understand better how to use the dictionaries in python and
how to form them in a way they can be accessible easily.
Finally, Python, Bottle, Jinja and Gzip documentations were used to search many built-in 
functions for the API.

Remarks:
--
I was not able to use properly the author_dict dictionary after all. In question number 3,
the route @app.route('/publications/<id:int>') is working properly, so in question number 4
in the server side router, another route was added (@app.route('/get_publication_info', method='POST'))
to demonstrate the use of the API and the server side as a whole. One can input a publication ID
in the corresponding form in the web interface, and the system will respond with a page with 
some information regarding the publication. The connection between the client and the server is 
successful, but not all routes were implemented successfully.
