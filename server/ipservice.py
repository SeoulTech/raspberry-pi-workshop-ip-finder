from protorpc import messages
import datetime

from protorpc import message_types
from protorpc import remote

from google.appengine.ext import ndb


class IpRecord(ndb.Model):
    """Models an individual device IP record """
    ip =  ndb.StringProperty()
    host =  ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class IpNote(messages.Message):
    """"Message in client-server RPC to track IP changes"""
    ip = messages.StringField(1, required=True)
    host = messages.StringField(2, required=False)
    when = messages.IntegerField(3)
    mac = messages.StringField(4, required=False)
    ssid = messages.StringField(5, required=False)



class IpService(remote.Service):

    # Add the remote decorator to indicate the service methods
    @remote.method(IpNote, message_types.VoidMessage)
    def post(self, request):

        # If the Note instance has a timestamp, use that timestamp
        if request.when is not None:
            when = datetime.datetime.utcfromtimestamp(request.when)

        # Else use the current time
        else:
            when = datetime.datetime.now()
        rIp = IpRecord(parent=ndb.Key('raspberry_ip_finder','2014'),
                       ip=request.ip,
                       host=request.host,
                       date=when)
        rIp.put()
        return message_types.VoidMessage()



