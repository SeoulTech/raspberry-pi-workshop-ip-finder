from protorpc.wsgi import service

import ipservice

# Map the RPC service and path (/ip)
ip_change_service = service.service_mappings([('/ip', ipservice.IpService)])



import webapp2
from ipservice import IpRecord
from google.appengine.ext import ndb

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('This is a list of PaspberryPi i know:\n')

        ip_records_query = IpRecord.query(
            ancestor=ndb.Key('raspberry_ip_finder','2014')).order(-IpRecord.date)
        ip_records = ip_records_query.fetch(10)

        for record in ip_records:
            self.response.write(
                '\n%s %s' % (record.ip, ' - ' + record.host if record.host else ''))


gui = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
