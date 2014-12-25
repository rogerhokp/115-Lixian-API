#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import getopt
import os
import sys
# import imp
# imp.reload(sys)
# sys.setdefaultencoding('utf-8')

from u115_api import u115_api

arg_user = None
arg_pass = None
arg_sleeptime = 120
asg_folder = None

 
def update_task_success(context):
    return open('tasksuccess.txt', 'a').write(context + '\n')

def update_task_error(context):
    return open('taskerror.txt', 'a').write(context + '\n')

def get_torrent_files():
    global asg_folder
    return [f for f in os.listdir(asg_folder ) if (os.path.isfile(f) and f.find('.torrent') != -1) ] 

def monitor():
    global arg_pass
    global arg_user
    global arg_sleeptime

    u115 = u115_api()
    u115.login(arg_user, arg_pass)
    torrents = get_torrent_files();


    logging.info('find Number of torrent %s in %s' % (len(torrents) , asg_folder) )

    for torrent in torrents:
        logging.info('\n************** adding torrent %s **************\n' % torrent)
        ret = u115.add_torrent_task(torrent)
        if ret : 
            os.remove(torrent)
            update_task_success('Torrent (%s) Added Success' % (torrent))
        else :
            update_task_error('Torrent (%s) Added Failed' % (torrent))

    input("Press Enter to continue...")
 
def Usage():
    print('115Bot usage:')
    print('-u, --user: 115 account login user')
    print('-p, --pass: 115 account login pass')
    print('-f, --folder: torrent folder path\n')
    print('-h, --help: print help message.')
    print('-v, --version: print script version')


def Version():
    print('115Bot ver 0.1')

def main(argv):
    global arg_pass
    global arg_user
    global arg_sleeptime
    global asg_folder

    try:
        opts, args = getopt.getopt(argv[1:], 'u:p:f:v:h', ['user=', 'pass=', 'file=', 'help', 'version'])
    except (getopt.GetoptError, err) as err:
        print(str(err))
        Usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif o in ('-u', '--user'):
            arg_user = a
        elif o in ('-p', '--pass'):
            arg_pass = a
        elif o in ('-f', '--folder'):
            asg_folder = a
        else:
            print('unhandled option')
            sys.exit(1)

    if arg_user is None:
        print('missing arg -u')
        sys.exit(2)
    if arg_pass is None:
        print('missing arg -p')
        sys.exit(2)

    asg_folder = asg_folder or '.'
    monitor()

if __name__ == '__main__':
    main(sys.argv)
