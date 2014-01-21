from protorpc.wsgi import service

import ipservice

# Map the RPC service and path (/ip)
ip_change_service = service.service_mappings([('/ip', ipservice.IpService)])



import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from ipservice import IpRecord

class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

        ip_records_query = IpRecord.query(
            ancestor=ndb.Key('raspberry_ip_finder','2014')).order(-IpRecord.date)
        ip_records = ip_records_query.fetch(10)


        template_values = {'token': 'not_impl_yet',
                           'me': user.user_id(),
                           'ips': ip_records,
                           'game_key': 'not_imp_yet'
                           }
#        for record in ip_records:
#            self.response.write(
#                '\n%s %s' % (record.ip, ' - ' + record.host if record.host else ''))

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

gui = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)


#TODO [x] switch to Jinja
#     [x] impl client.go
#     [x]  - POST JSON to URL raspberry-pi-workshop.appengine.com
#     add websocket support for server
#     add /get with re-direct to intaller on github
#     add install_client.sh
#       - downloads client.py
#       - downloads ip-finder-deamon.sh
#       - places it /etc/init.d
#       - start it up
#       - add it to runlevel to run on boot
#     add wildcard CNAME to seoultechsociety.org, pointing on GAE
# 
