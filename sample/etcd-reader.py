# This code is used for "internal docker container" read/write value at etcd.
#
# CoreOS (etcd Activated)
#   |                 ^
#   |   NAT           | iptables
#   V                 |
# Docker Container -> python code.
#
# This can be used for "distriburted or HA environment"

import requests
import json

class etcd:
  def __init__(self, ips="169.254.169.255", ports=4001):
    self.ips = ips
    self.ports = ports
  def get(self, keys):
    try:
      urls = "http://%s:%d/v2/keys/%s" % (self.ips, self.ports , keys.strip("/"))
      res = requests.get(urls)
      if res.status_code == 200: # Found
        return json.loads(res.content)["node"]["value"]
      elif res.status_code == 404: # Not Found
        return None
    except:
      pass
    return None
  def put(self, keys, values):
    try:
      urls = "http://%s:%d/v2/keys/%s" % (self.ips, self.ports , keys.strip("/"))
      res = requests.put(urls, {"value": values})
      if res.status_code == 200: # Modified
        return True
      elif res.status_code == 201: # Create
        return True
    except:
      pass
    return False
  def delete(self, keys):
    try:
      urls = "http://%s:%d/v2/keys/%s" % (self.ips, self.ports , keys.strip("/"))
      res = requests.delete(urls)
      if res.status_code == 200:
        return True
    except:
      pass
    return False

# code under this is for using etcd.
c = etcd()
c.get("asdf")
c.put("asdf","asdf")
c.put("asdf","asdf1")
c.get("asdf")
c.delete("asdf")
