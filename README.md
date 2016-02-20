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

The following methods were added to conference.py to perform Session methods including create and query functionality. The first two I designed as private methods because they should only be able to be called by the endpoints. The endpoints are callable from HTML. I designed Sessions to have an ancestor relationship to the Conference to which it belongs. The Session relationship then has a "Has A" relatinoship to the speaker. The speaker is a property of the Session. I did this because I chose the efficiency of fewer "Kinds" in my data store and therefor fewer Entities. I don't see the utility of creating a new class for Speakers other than adding additional functions for booking hotels for them, contact information etc. For now I beleive my structure is the most efficient. 
My Session model utilizes the StringProperty for name, highlights, speaker, typeOfSession, location, and websafeKey. The SessionForm uses an EnumField for typeOfSession to limit the types of sessions allowed in Session entities. Name is the only required field allowing a planner to map out some session types without knowing all the details like time, room, speaker, etc. Other properties utilize other property types. For example, startTime is a TimeProperty, and date is a DateProperty. This allows other functionality used in queries in conference.py. I also enforce the time property in the _createSessionObject function by forcing it to be a python '.time()' object. Lastly, my application stores durationInMinutes as an IntegerProperty so future enhancements can do things like add the times together to get a 'total conference time' or help an attendee schedule their day.
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
For this task I chose to create two additional tasks. The first additional task I created is getSessionsByDateTimeLocation(). This function will be usefull in seeing if a room (location) has been doule booked. The second function I created is getSessionsByLocation(). This session would help the organizer assign people to certain rooms to make sure they are ready. For example, I might need to provide the maintenance crew with the results of this query so they can assign the right staff to prepare the room. 

Lastly, getAllNonWorkshopsBefore7PM(), solves the problem of "Let’s say that you don't like workshops and you don't like sessions after 7 pm." The method first filters workshops that are Keynote of Lectures using an equality filter. Then it filters sessions starting after 7 by filtering results by an inequality. I used the Python documentation to create a time object that I used an inequality filter on. Lastly I ordered the results by time. This is the best way that I can think of to impliment this problem because the first Index rule is inequality filters can be applied to only one property. 