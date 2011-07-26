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

        self.returnvalue = None

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

    def finished(self):
        value =  self.process.poll()
        if value == None:
            return False
        else:
            self.return_value = value
            return True

    def communicate(self):
        return self.process.communicate()

    def get_image(self):
        return os.path.join(self.workingdir, self.outputfile)

    def __del__(self):
        self.cleanup()


def main():
    data1 = {}
    data1['inputfile']  = 'fractal2.pov'
    data1['outputfile'] = 'output.png'
    data1['width']      = '1920'
    data1['height']     = '1920'
    data1['start']      = '1'
    data1['end']        = '960'
    data1['extras']     = ["+FN", "-GA", "-D", "-V"]

    data2 = {}
    data2['inputfile']  = 'fractal2.pov'
    data2['outputfile'] = 'output.png'
    data2['width']      = '1920'
    data2['height']     = '1920'
    data2['start']      = '961'
    data2['end']        = '1920'
    data2['extras']     = ["+FN", "-GA", "-D", "-V"]

    config_json1 = json.dumps(data1)
    config_json2 = json.dumps(data2)

    print "create povray process object"
    pov_processes = {}
    pov_processes[1] = Povray(config_json1, 1)
    pov_processes[2] = Povray(config_json2, 2)
    pov_processes[1].create_args()
    pov_processes[2].create_args()
    print pov_processes[1].args
    print pov_processes[2].args
    pov_processes[1].setup()
    pov_processes[2].setup()
    pov_processes[1].run()
    pov_processes[2].run()
    while 1:
        if len(pov_processes) == 0:
            sys.exit()
        process_list = pov_processes.copy()
        for number, process in process_list.iteritems():
            pollval = process.finished()
            print "%i  %s" % (number, pollval)
            if pollval == True:
                print process.communicate()
                del(pov_processes[number])
        sleep(1)



if __name__ == '__main__':
    main()


