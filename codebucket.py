#Conference websafekeys:
ahpkZXZ-Y29uZmVyZW5jZWNlbnRyYWwtMTE4NHI0CxIHUHJvZmlsZSIXcm9iZXJ0a29obDEyNUBnbWFpbC5jb20MCxIKQ29uZmVyZW5jZRgBDA

#Session websafekeys:
ahpkZXZ-Y29uZmVyZW5jZWNlbnRyYWwtMTE4NHIdCxIKQ29uZmVyZW5jZRgBDAsSB1Nlc3Npb24YBAw
ahpkZXZ-Y29uZmVyZW5jZWNlbnRyYWwtMTE4NHIdCxIKQ29uZmVyZW5jZRgBDAsSB1Nlc3Npb24YBQw
ahpkZXZ-Y29uZmVyZW5jZWNlbnRyYWwtMTE4NHIdCxIKQ29uZmVyZW5jZRgCDAsSB1Nlc3Npb24YBgw


#  ------------
#  |  TASK 2  |
#  ------------
    @endpoints.method(WISHLIST_POST_REQUEST, SessionForm,
            http_method='GET', name='getSessionsInWishlist')
    def getSessionsInWishlist(self, request):
        """Checks for authed user, query for all the sessions in a conference that the user is interested in, open to all conferences."""

        # make sure user is authed
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        user_id = getUserId(user)
        return user


#  ------------
#  |  TASK 2  |
#  ------------
    @endpoints.method(WISHLIST_POST_REQUEST, SessionForm,
            http_method='DELETE', name='deleteSessionInWishlist')
    def deleteSessionInWishlist(self, request):
        """Checks for authed user, removes the session from the user’s list of sessions they are interested in attending."""

        # make sure user is authed
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        user_id = getUserId(user)
        return user




 
    @ndb.transactional(xg=True)
    def _sessionWishlist(self, request, addTo=True):
        """Add or remove session from users wishlist."""
        retval = None

        # Fetch user Profile
        prof = self._getProfileFromUser()

        # Fetch Session and check if session exists given websafeSessionKey
        wsck = request.websafeSessionKey
        sess = ndb.Key(urlsafe=wsck).get()
        if not sess:
            raise endpoints.NotFoundException(
                'No session found with key: %s' % wsck)

        # Check if session is already in wishlist otherwise add
        if addTo:
            if wsck in prof.wishlistSessionKeys:
                raise ConflictException("You have already added this session to your wishlist")
            retval = True

        # Check if session is in wishlist then remove
        else:
            if wsck in prof.wishlistSessionKeys:
                prof.wishlistSessionKeys.remove(wsck)
                retval = True
            else:
                retval = False

        # Put back in datastore and return
        prof.put()
        return BooleanMessage(data=retval)


    @endpoints.method(WISHLIST_POST_REQUEST, BooleanMessage, path='session/{websafeSessionKey}/wishlist', http_method='POST', name='addSessionToWishlist')
    def addSessionToWishlist(self, request):
        """Register user for selected conference."""
        return self._sessionWishlist(request)


# uses form, based on the update profile method
    def _updateProfileObject(self, request):

        # Copy ProfileForm/ProtoRPC Message into dict
        data = {field.name: getattr(request, field.name) for field in request.all_fields()}

        # Get existing profile
        prof = self._getProfileFromUser()

        # Not getting all the fields, so don't create a new object; just
        # copy relevant fields from WishlistForm to Profile object
        for field in request.all_fields():
            data = getattr(request, field.name)
            # only copy fields where we get data
            if data not in (None, []):
                # write to Profile object
                setattr(prof, field.name, data)
        prof.put()
        return self._copyProfileToForm(prof)


    #Takes input from ProfileForm and passes it as request to _updateProfileObject
    @endpoints.method(ProfileForm, ProfileForm, path='profile/{websafeSessionKey}', http_method='POST', name='addSessionToWishlist')
    def addSessionToWishlist(self, request):
        """Checks for authed user, adds the session to the user's list of sessions they are interested in attending."""

        # make sure user is authed
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        # Send request to _updateProfileObject
        return self._updateProfileObject(request)

    @endpoints.method(SESS_GET_REQUEST, ConferenceForms,  path='session/featuredSpeaker', http_method='GET', name='getFeaturedSpeaker')
    def getFeaturedSpeaker(self, request):
        """Return Featured speaker announcement from memcache. 
        The featured speaker is defined to be the speaker with the most sessions.
        """

        # Fetch websafeConferenceKey from request 
        conf = ndb.Key(urlsafe=request.websafeConferenceKey).get()

        # Check that conference exists
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with key: %s' % request.websafeConferenceKey)

        # Fetch conference data by copying SessionForm/ProtoRPC Message into dict
#        data = {field.name: getattr(request, field.name) for field in request.all_fields()}
        c = Conference.query(projection=[Conference.featuredSpeaker])

        # Perform ancestor query with projection query
        sessions = Session.query(ancestor=ndb.Key(Conference, conf.key.id()), projection=[Session.speaker])
        print sessions

        # Put results in a dictionary
        speakers = []
        for s in sessions:
            speakers.append(s)
        print speakers
#       return SessionForms(items=[self._copySessionToForm(s) for s in sessions])

#        conference = Conference.query(ndb.AND(Session.seatsAvailable <= 5, Conference.seatsAvailable > 0)).fetch(projection=[Conference.name])
        return ConferenceForms(items=[self._copyConferenceToForm(conf, '') for conf in c])

        #StringMessage(data=memcache.get(MEMCACHE_FEATURED_SPEAKER_KEY) or "")

        
    def _addFeaturedSpeaker(self, request):
        """Add speaker as featuredSpeaker to Conference."""

        getFeaturedSpeaker()
        data = {field.name: getattr(request, field.name) for field in request.all_fields()}
        speaker = data['speaker']
        conf = ndb.Key(urlsafe=wsck).get()

        conf.featuredSpeaker.append(speaker)
        conf.put()

        announcement = ('This conferences featured speaker is %s!', speaker)
        memcache.set(MEMCACHE_FEATURED_SPEAKER_KEY, announcement)
        return announcement