Api to communicate with Vola
----------------------------
----------------------------
The purpose of building this API was to provide information about the events
in VMS to Vola so that their volunteers could participate in them. Presently,
these fields of events are sent to Vola via the API::

1. Event Name - Title or name of the event.
2. Start Date - The date from which the event would start.
3. End Date - The date on which the event would end.
4. Description - The details of the event.
5. Address - The address on which event would take place.
6. City - The city where event would take place.
7. State - The state where event would take place.
8. Country - The country where event would take place.
9. Venue - The location of the event.

 Users can send in a ``GET`` or a ``POST`` request to <https://localhost/event/api/v1/request_event_data/> to access the event data.
 
 In case of a ``GET`` request, a list containing the details of all events
in the ascending order of their start dates will be returned :

 <img src="/docs/screenshots/GET_Vola.png">

In case of a ``POST`` request,a list containing the details of all events
starting after the date value sent in the request object will be returned :
 
<img src="/docs/screenshots/POST_Vola.png">

 Details of the API
------------------
 1. Use Case : Send event details for volunteers to contribute accordingly.

 2. API Method : GET/POST

 3. URL Parameters : https://localhost/event/api/v1/request_event_data/

 4. Request Body::<br>
       {<br>
        "Date” : “date after which all events are required (yyyy-mm-dd)”<br>
      }

 5. Response Body - Success::<br>
       {<br>
        “Event Name/Title” : “ --------”<br>
        “Start Date” : “-----------”<br>
        “End Date” : “-----------”<br>
        “Description” : “-----------”<br>
        “Address” : “-----------”<br>
        “City” : “-----------”<br>
        “State” : “-----------”<br>
        “Country” : “-----------”<br>
        “Venue” : “------------------”<br>
      }

 6. Response Body - Error::<br>
       {<br>
        "message": "Please input a proper date"<br>
      }
