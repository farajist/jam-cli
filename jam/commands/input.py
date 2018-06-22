"""The input command."""


import requests
import os.path as osp
import predictionio
import datetime
import random
import pytz
from .base import Base

RATE_ACTIONS_DELIMITER = ","
PROPERTIES_DELIMITER = ":"
SEED = 1
class Input(Base):
    """Say input, world!"""

    def run(self):

		
        # print('here we arre')
        PATH = "/Users/Hamza07/Desktop/rec_apps/"
        with open(osp.join(PATH, self.options['<app_name>'], 'access_key'), 'r') as myfile:
            data = myfile.read()
        accessKey = data.replace('\n', '')
        # print(accessKey)
        # url = "http://localhost:7070/events.json?accessKey=" + accessKey

        current_date = datetime.datetime.now(pytz.utc)

        client = predictionio.EventClient(accessKey, "http://localhost:7070", threads=5, qsize=500)
        if (self.options['<datafile>'] is not None):
			self.import_events(client, self.options['<datafile>'])	
        else:
            client.create_event(
                event=self.options['<action>'],
                entity_type="user",
                entity_id=self.options['<user_id>'],
                target_entity_type="item",
                target_entity_id=self.options['<item_id>'],
                event_time = current_date
            )
        
            print("[jam] created event: " + self.options['<action>'] + " entity_id: " + self.options['<user_id>'] + " target_entity_id: " + self.options['<item_id>'] + \
                " current_date: " + current_date.isoformat())

    def import_events(self, client, file):
        f = open(file, 'r')
        random.seed(SEED)
        count = 0
		# year, month, day[, hour[, minute[, second[
		#event_date = datetime.datetime(2015, 8, 13, 12, 24, 41)
        now_date = datetime.datetime.now(pytz.utc) # - datetime.timedelta(days=2.7)
        current_date = now_date
        event_time_increment = datetime.timedelta(days= -0.8)
        available_date_increment = datetime.timedelta(days= 0.8)
        event_date = now_date - datetime.timedelta(days= 2.4)
        available_date = event_date + datetime.timedelta(days=-2)
        expire_date = event_date + datetime.timedelta(days=2)
        print("Importing data...")

        for line in f:
            data = line.rstrip('\r\n').split(RATE_ACTIONS_DELIMITER)
			# For demonstration purpose action names are taken from input along with secondary actions on
			# For the UR add some item metadata

            if (data[1] != "$set"):
                client.create_event(
				    event=data[1],
				    entity_type="user",
				    entity_id=data[0],
				    target_entity_type="item",
				    target_entity_id=data[2],
				    event_time = current_date
			    )
                print("Event: " + data[1] + " entity_id: " + data[0] + " target_entity_id: " + data[2] + \
                    " current_date: " + current_date.isoformat())
            elif (data[1] == "$set"):  # must be a set event
                properties = data[2].split(PROPERTIES_DELIMITER)
                prop_name = properties.pop(0)
                prop_value = properties if not prop_name == 'defaultRank' else float(properties[0])
                client.create_event(
				    event=data[1],
				    entity_type="item",
				    entity_id=data[0],
				    event_time=current_date,
				    properties={prop_name: prop_value}
                )
                print("Event: " + data[1] + " entity_id: " + data[0] + " properties/"+prop_name+": " + str(properties) + \
                    " current_date: " + current_date.isoformat())
                count += 1
                current_date += event_time_increment

            items = ['Iphone X', 'Ipad-retina', 'Nexus', 'Surface', 'Iphone 8', 'Galaxy', 'Iphone 7']
            print("All items: " + str(items))
            for item in items:
                client.create_event(
                    event="$set",
                    entity_type="item",
                    entity_id=item,
                    properties={"expires": expire_date.isoformat(),
                        "available": available_date.isoformat(),
                        "date": event_date.isoformat()}
                    )
                print("Event: $set entity_id: " + item + \
					" properties/availableDate: " + available_date.isoformat() + \
					" properties/date: " + event_date.isoformat() + \
                    " properties/expireDate: " + expire_date.isoformat())
                expire_date += available_date_increment
                event_date += available_date_increment
                available_date += available_date_increment
                count += 1

        f.close()
        print("%s events are imported." % count)