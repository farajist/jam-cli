"""The init command."""


from json import dumps
from os.path import expanduser
import os.path as osp
from git import Repo
# from subprocess import call
import subprocess

from .base import Base


class Init(Base):
    """init an engine!"""

    def run(self):
        print('[init command] You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
        o_path = self.options['PATH']
        path = o_path if o_path else expanduser("~/Desktop/rec_apps")
        repo = Repo.clone_from('https://github.com/actionml/universal-recommender.git', osp.join(path, self.options['<name>']))
        
        try:
            subprocess.call(['pio app new ' + self.options['<name>']], shell=True)
        except subprocess.CalledProcessError:
            print("[jam] couldn't create app")
        try:
            pioapp = subprocess.Popen(('pio', 'app', 'show', self.options['<name>']), stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print("[jam] couldn't list apps")
        try:
            print('This is grep')
            grep = subprocess.Popen(('grep', 'Key'), stdin=pioapp.stdout, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print("[jam] couldn't grep apps")
        try:
            cutAK = subprocess.check_output(('cut', '-f', '7', '-d', ' '), stdin=grep.stdout)
            print("Storing access key to file : " + cutAK)
            with open(osp.join(path, self.options['<name>'], 'access_key'), 'w') as file:
                file.write(cutAK)
        except subprocess.CalledProcessError:
            print("[jam] couldn't extract access key")
        