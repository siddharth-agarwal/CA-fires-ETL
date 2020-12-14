import csv
import requests
from geojson import Feature, FeatureCollection, Point

def get_fires():
  lines = requests.get("http://www.fire.ca.gov/imapdata/mapdataactive.csv").content.decode('utf-8').splitlines()
  reader = csv.DictReader(lines, delimiter=',')

  tidy_reader = []
  for row in reader:
    tidy_reader.append(dict((k.strip(), v.strip()) for k, v in row.items()))

  features = [Feature(geometry=Point(map(float, [r['incident_longitude'], r['incident_latitude']])),properties=r) for r in tidy_reader]

  return FeatureCollection(features)

fire_data= get_fires()

## can wrap these into FeatureCollection() objects
active_fires = [f for f in fire_data['features'] if f['properties']['is_active'] == 'Y']

inactive_fires = [f for f in fire_data['features'] if f['properties']['is_active'] == 'N']