"""The trace command."""


from json import dumps
import os.path as osp
import json
from .base import Base
# from .. import Engine

class Trace(Base):
    """Say trace, world!"""

    def run(self):
        path = "/Users/Hamza07/Desktop/rec_apps/"
        print('[trace command] You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        e = self.getInstance()
        l = [self.options['<primary_event>'], self.options['<se_1>']]
        l += self.options['<se_2>']
        
        e['datasource']['params']['eventNames'] = l
        e['datasource']['params']['appName'] = self.options['<app_name>']
        e['algorithms']['params']['appName'] = self.options['<app_name>']

        for a in range(len(e['algorithms'])):
			e['algorithms'][a]['params']['indicators'] = []

        for a in range(len(e['algorithms'])):
            e['algorithms'][a]['params']['indicators'].append({
				'name' : l[0] 
            })
            for i in range(1, len(l)):
                e['algorithms'][a]['params']['indicators'].append({
                    'name': l[i],
                    'maxCorrelatorsPerItem' : 50
                })

        print(e['algorithms'][0]['params']['indicators'])
        with open(osp.join(path, self.options['<app_name>'], 'engine.json'), 'a+') as outfile:
            json.dump(e, outfile)

    def getInstance(self):
		jsonData = ENGINE_JSON
		obj = json.loads(jsonData)
		return obj

ENGINE_JSON="""
	{
		"comment":" This config file uses default settings for all but the required values see README.md for docs",
		"id": "default",
		"description": "Default settings",
		"engineFactory": "com.actionml.RecommendationEngine",
		"datasource": {
			"params" : {
			"name": "sample-handmade-data.txt",
			"appName": "jamrec",
			"eventNames": ["purchase", "view", "category-pref"],
			"minEventsPerUser": 3
			}
		},
		"sparkConf": {
			"spark.serializer": "org.apache.spark.serializer.KryoSerializer",
			"spark.kryo.registrator": "org.apache.mahout.sparkbindings.io.MahoutKryoRegistrator",
			"spark.kryo.referenceTracking": "false",
			"spark.kryoserializer.buffer": "300m",
			"es.index.auto.create": "true"
		},
		"algorithms": [
			{
			"comment": "simplest setup where all values are default, popularity based backfill, must add eventsNames",
			"name": "ur",
			"params": {
				"appName": "jamrec",
				"indexName": "urindex",
				"typeName": "items",
				"comment": "must have data for the first event or the model will not build, other events are optional",
				"indicators": [
				{
					"name": "purchase"
				},{
					"name": "view",
					"maxCorrelatorsPerItem": 50
				},{
					"name": "category-pref",
					"maxCorrelatorsPerItem": 50
				}
				],
				"availableDateName": "available",
				"expireDateName": "expires",
				"dateName": "date",
				"num": 4
			}
			}
		]
	}
	"""