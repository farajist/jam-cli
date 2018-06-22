"""The deploy command."""



import os.path as osp
import subprocess
from .base import Base


class Deploy(Base):
    """Say deploy, world!"""

    def run(self):
        PATH = "/Users/Hamza07/Desktop/rec_apps/"
        try:
            subprocess.call(['pio build --clean'], shell=True, 
			cwd=osp.join(PATH, self.options['<app_name>']))
        except subprocess.CalledProcessError:
            print("[jam] couldn't build app")

        try:
            subprocess.call(['pio train -- --executor-memory 4g --driver-memory 4g'], shell=True, 
			cwd=osp.join(PATH, self.options['<app_name>']))
        except subprocess.CalledProcessError:
            print("[jam] couldn't train app")


        try:
            subprocess.call(['pio deploy& '], shell=True, 
			cwd=osp.join(PATH, self.options['<app_name>']))
        except subprocess.CalledProcessError:
            print("[jam] couldn't deploy app")