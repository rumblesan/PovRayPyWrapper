#!/usr/bin/env python

from subprocess import Popen, PIPE
from time import sleep
import sys
import os
import json
import shutil


class Povray():

    process      = None
    args         = []
    return_value = None
    completed    = False

    def __init__(self, config_json, node_number):

        config_info = json.loads(config_json)

        self.node_number = node_number
        self.workingdir  = "/var/PovNode/node" + str(self.node_number)

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
        value =  self.process.poll()
        if value == None:
            return False
        else:
            self.return_value = value
            self.completed = True
            return True

    def communicate(self):
        return self.process.communicate()

    def get_image(self):
        return os.path.join(self.workingdir, self.outputfile)

    def __del__(self):
        self.cleanup()

class ProcessManager():

    process_list = []
    process_num  = 1
    debug        = False
    running      = 0

    def __init__(self, debug):
        self.debug = debug

    def new_process(self, config_json):
        new_process = Povray(config_json, self.process_num)
        new_process.setup()
        new_process.create_args()
        new_process.run()
        self.process_list.append(new_process)
        if self.debug:
            print "Process %i added" % self.process_num
        self.process_num += 1
        self.running += 1

    def check_processes(self):
        for process in self.process_list:
            poll_value = process.poll()
            if self.debug:
                print "Process %i poll is %s" % (process.node_number, poll_value)

    def clear_processes(self):
        finished = [process for process in self.process_list if process.completed]
        self.process_list = [process for process in self.process_list if not process.completed]
        self.running -= len(finished)
        if self.debug:
            print "%i processes finished" % len(finished)
        for process in finished:
            print "%i  %s" % (process.node_number, process.get_image())
        if self.debug:
            print "%i processes still running" % len(self.process_list)

def main():
    data = {}
    data['inputfile']  = 'fractal2.pov'
    data['outputfile'] = 'output.png'
    data['width']      = '1920'
    data['height']     = '1920'
    data['start']      = '1'
    data['end']        = '1920'
    data['extras']     = ["+FN", "-GA", "-D", "-V"]

    config_json = json.dumps(data)

    print "create process manager object"
    manager = ProcessManager(True)
    manager.new_process(config_json)
    #manager.new_process(config_json)
    #manager.new_process(config_json)
    #manager.new_process(config_json)
    while 1:
        manager.check_processes()
        manager.clear_processes()
        sleep(1)



if __name__ == '__main__':
    main()


