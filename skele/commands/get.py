"""The get command."""


from json import dumps
import predictionio
import os.path as osp
from .base import Base


class Get(Base):
    """Say get, world!"""

    def run(self):
        PATH = "/Users/Hamza07/Desktop/rec_apps/"
        with open(osp.join(PATH, self.options['<app_name>'], 'access_key'), 'r') as myfile:
            data = myfile.read()
        accessKey = data.replace('\n', '')
        engine_client = predictionio.EngineClient(url='http://localhost:8000',)
        result = engine_client.send_query(data={"uid": self.options['<user_id>'], "n" : self.options['<num_recs>']})
        # print(request)
        # try:
        # result = request.get_response() # check the request status and get the return data.
        print(result)
        # except:
            # print('[jam] there was an error fetching recommendations')