#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import getopt
import os
import sys
import shutil
import tempfile
import time
import datetime
import codecs
# import imp
# imp.reload(sys)
# sys.setdefaultencoding('utf-8')

from u115_api import u115_api

arg_user = None
arg_pass = None
arg_sleeptime = 120
arg_folder = None


 
def update_task_success(context):
    return codecs.open('tasksuccess.txt', 'a', "utf-8").write(str(datetime.datetime.now()) + ' : ' + context + '\n')

def update_task_error(context):
    return codecs.open('taskerror.txt', 'a', "utf-8").write(str(datetime.datetime.now()) + ' : ' + context + '\n')

def get_torrent_files():
    global arg_folder
    return [f for f in os.listdir(arg_folder ) if ( os.path.isfile(os.path.join(arg_folder, f)) and f.find('.torrent') != -1) ] 

def copy_torrent_tmp_file(torrent, tempFolder):
    global arg_folder
    copyTo = os.path.join(tempFolder, '',  str(int(time.time())) + '.torrent' )
    shutil.copyfile(os.path.join(arg_folder, torrent),copyTo)
    return copyTo

def monitor():
    global arg_pass
    global arg_user
    global arg_sleeptime

    u115 = u115_api()
    u115.login(arg_user, arg_pass)
    torrents = get_torrent_files();
    tempFolder = tempfile.mkdtemp();

    logging.info('find Number of torrent %s in %s' % (len(torrents) , arg_folder) )
    try : 
        for torrent in torrents:
                logging.info('\n************** adding torrent %s **************\n' % torrent)
                tmpFile = copy_torrent_tmp_file(torrent,tempFolder)
                ret = u115.add_torrent_task(tmpFile)
                if ret : 
                    os.remove(os.path.join(arg_folder, torrent))
                    update_task_success('Torrent (%s) Added Success' % (torrent))
                else :
                    update_task_error('Torrent (%s) Added Failed' % (torrent))
    finally :
        logging.info('clearing temp folder %s' % tempFolder)
        shutil.rmtree(tempFolder)

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
    global arg_folder

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
            arg_folder = a
        else:
            print('unhandled option')
            sys.exit(1)

    if arg_user is None:
        print('missing arg -u')
        sys.exit(2)
    if arg_pass is None:
        print('missing arg -p')
        sys.exit(2)

    arg_folder = arg_folder or '.'
    monitor()

if __name__ == '__main__':
    main(sys.argv)
