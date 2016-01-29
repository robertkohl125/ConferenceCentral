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

One interesting choice I made was to define an independent ResourceContainer for each Session HTML GET request. I did this for simplicity to 
##### Session HTML GET request ResourceContainers:
1. SESS_GET_REQUEST
1. SESS_GET_REQUEST_TOS 
1. SESS_GET_REQUEST_SPKR 