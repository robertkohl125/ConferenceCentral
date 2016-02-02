ahpkZXZ-Y29uZmVyZW5jZWNlbnRyYWwtMTE4NHI1CxIHUHJvZmlsZSIXcm9iZXJ0a29obDEyNUBnbWFpbC5jb20MCxIKQ29uZmVyZW5jZRjpBww

Bob Marley
ahhzfmNvbmZlcmVuY2VjZW50cmFsLTExODRyNgsSB1Byb2ZpbGUiF3JvYmVydGtvaGwxMjVAZ21haWwuY29tDAsSCkNvbmZlcmVuY2UYgfEEDA

ahpkZXZ-Y29uZmVyZW5jZWNlbnRyYWwtMTE4NHI0CxIHUHJvZmlsZSIXcm9iZXJ0a29obDEyNUBnbWFpbC5jb20MCxIKQ29uZmVyZW5jZRgBDA

ahhzfmNvbmZlcmVuY2VjZW50cmFsLTExODRyNgsSB1Byb2ZpbGUiF3JvYmVydGtvaGwxMjVAZ21haWwuY29tDAsSCkNvbmZlcmVuY2UYgfEEDA


sessionkey
ahpkZXZ-Y29uZmVyZW5jZWNlbnRyYWwtMTE4NHIfCxIKQ29uZmVyZW5jZRjpBwwLEgdTZXNzaW9uGNoPDA

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