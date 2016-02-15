import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from conference import ConferenceApi


class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache.
        """
        ConferenceApi._cacheAnnouncement()


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation.
        """
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
            )


class SendConfirmationEmailHandler2(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Session creation.
        """
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Session!',               # subj
            'Hi, you have created a following '         # body
            'session:\r\n\r\n%s' % self.request.get(
                'sessionInfo')
            )

class SetFeaturedSpeakerHandler(webapp2.RequestHandler):
    def post(self):
        """Set Featured Speaker in Conferences.
        """
        ConferenceApi._doFeaturedSpeaker()

app = webapp2.WSGIApplication([
	('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/send_confirmation_email2', SendConfirmationEmailHandler2),
    ('/tasks/set_featured_speaker', SetFeaturedSpeakerHandler)
    ], debug=True)
