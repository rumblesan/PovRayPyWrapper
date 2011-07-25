#!/usr/bin/env python

from subprocess import Popen, PIPE
from time import sleep
import sys
import os
import json
import shutil


class Povray():

    def __init__(self, config_json, node_number):

        config_info = json.loads(config_json)

        self.node_number = node_number
        self.workingdir  = "/var/PovNode/node" + str(self.node_number)

        self.process     = ""
        self.args        = []

        self.command     = "povray"

        self.extras      = config_info['extras']

        self.inputfile   = config_info['inputfile']
        self.outputfile  = config_info['outputfile']

        self.width       = config_info['height']
        self.height      = config_info['width']

        self.start_col   = config_info['start']
        self.end_col     = config_info['end']

    def create_args(self):
        self.args.append(self.command)
        self.args.append("+I" + self.inputfile)
        self.args.append("+O" + self.outputfile)
        self.args.append("+W" + self.width)
        self.args.append("+H" + self.height)
        self.args.append("+SC" + self.start_col)
        self.args.append("+EC" + self.end_col)
        self.args.extend(self.extras)

    def setup(self):
        if os.path.exists(self.workingdir):
            shutil.rmtree(self.workingdir)
        os.makedirs(self.workingdir)
        shutil.copy(self.inputfile, os.path.join(self.workingdir, self.inputfile))
        os.chdir(self.workingdir)

    def cleanup(self):
        os.chdir('..')
        shutil.rmtree(self.workingdir)

    def run(self):
        self.process = Popen(self.args, stdin=None, stdout=PIPE, stderr=PIPE)

    def poll(self):
        return self.process.poll()

    def communicate(self):
        return self.communicate.poll()


data = {}
data['inputfile']  = 'fractal2.pov'
data['outputfile'] = 'output.png'
data['height']     = '768'
data['width']      = '1024'
data['start']      = '1'
data['end']        = '1024'
data['extras']     = ["+FN", "-GA", "-D", "-V"]

config_json = json.dumps(data)

print "create povray process object"
povproc = Povray(config_json, 1)
povproc.create_args()
print povproc.args
povproc.setup()
povproc.run()
while 1:
    pollval = povproc.poll()
    print pollval
    if pollval == 0:
        sys.exit()
        print povproc.communicate()
    sleep(1)





