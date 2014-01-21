from protorpc import messages
import datetime

from protorpc import message_types
from protorpc import remote

from google.appengine.ext import ndb


class IpRecord(ndb.Model):
    """Models an individual device IP record """
    ip =  ndb.StringProperty()
    host = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    mac = ndb.StringProperty()


class IpNote(messages.Message):
    """"Message in client-server RPC to track IP changes"""
    IP = messages.StringField(1, required=True)
    Host = messages.StringField(2)
    When = messages.IntegerField(3)
    MAC = messages.StringField(4)
    SSID = messages.StringField(5)



class IpService(remote.Service):

    # Add the remote decorator to indicate the service methods
    @remote.method(IpNote, message_types.VoidMessage)
    def post(self, request):

        # If the Note instance has a timestamp, use that timestamp
        if request.When:
            when = datetime.datetime.utcfromtimestamp(request.When)

        # Else use the current time
        else:
            when = datetime.datetime.now()
        rIp = IpRecord(parent=ndb.Key('raspberry_ip_finder','2014'),
                       ip=request.IP,
                       host=request.Host,
                       date=when,
                       mac=request.MAC)
        rIp.put()
        return message_types.VoidMessage()



