App Engine application for the Udacity training course.

#### Products
- [App Engine][1]

#### Language
- [Python][2]

#### APIs
- [Google Cloud Endpoints][3]

#### Links
- [App Engine Console][7]
- [API Explorer][8]

#### Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
1. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
1. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
1. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
1. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting
   your local server's address (by default [localhost:8080][5].)
1. Generate your client library(ies) with [the endpoints tool][6].
1. Deploy your application.


[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:8080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool
[7]: https://console.developers.google.com/project
[8]: https://apis-explorer.appspot.com/apis-explorer/?base=https://conferencecentral-1184.appspot.com/_ah/api#p/


#### Task 1: Design Choices

The following methods were added to conference.py to perform Session methods including create and query functionality. The first two I designed as private methods because they should only be able to be called by the endpoints. The endpoints are callable from HTML.
##### Private methods:
1. _copySessionToForm(self, session)
1. _createSessionObject(self, request)

##### Endpoints:
2. createSession(self, request)
2. getConferenceSessions(self, request)
2. getConferenceSessionsByType(self, request)
2. getSessionsBySpeaker(self, request)

I currently have the _createSessionObject limited to logged in users rather than the createSession endpoint.

One interesting choice I made was to define an independent ResourceContainer for each Session HTML GET request. I did this for simplicity to 
##### Session HTML GET request ResourceContainers:
1. SESS_GET_REQUEST
1. SESS_GET_REQUEST_TOS 
1. SESS_GET_REQUEST_SPKR 

Task #3
For this task I chose to create two additional tasks. The first additional task I created is getSessionsByDateTimeLocation(). This function will be usefull in seeing if a room (location) has been doule booked. The second function I created is getSessionsByLocation(). This session would help the organizer assign people to certain rooms to make sure they are ready. For example, I might need to provide the maintenance crew with the results of this query so they can assign the right staff to prepare the room. Lastly, getAllNonWorkshopsBefore7PM(), filters out all workshops after 7 by filtering results by an equality filter using "or". Then I used the Python documentation to create a time object that I used to filter by time. This is the best way that I can think of to impliment this problem because the first Index rule is Inequality filters can be applied to only one property. 