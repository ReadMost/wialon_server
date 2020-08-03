import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
import datetime
import pyproj
from shapely.geometry import Point
from shapely.ops import transform

from db.base import session
from db.models import ShortPacket, BlackBoxPacket

project = lambda x, y: pyproj.transform(pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:3857'), x, y)


def transform_geom(long, lat):
	try:
		return transform(project, Point(float(long), float(lat)))
	except Exception as e:
		print(str(e))

class ShortRequestSession(object):


	@staticmethod
	def save_data(date_time, point, speed, course, alt, sats, black_box, imei,  *args, **kwargs):
		sh_req = ShortPacket(date_time=date_time, point="SRID=3857;" + transform_geom(point[1], point[0]).wkt,
		                     speed=speed, course=course, alt=alt, sats=sats, black_box=black_box, imei=imei)
		session.add(sh_req)
		session.commit()

class BlackBoxSession(object):

	def __init__(self):
		self.instance = BlackBoxPacket(0, 0)
		self.instance.save()

	def save(self, new_was_send = None, new_was_processed=None):
		self.instance.was_send = new_was_send if new_was_send else self.instance.was_send
		self.instance.was_proceeded = new_was_processed if new_was_processed else self.instance.was_proceeded
		self.instance.save()

	def get(self):
		return self.instance
