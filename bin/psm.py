#! /usr/bin/env python
# Copyright (C) 2004 - 2017 Keysight Technologies, Inc


import os
import sys
import string
import re
import subprocess

import getpass
import socket
import datetime

def usage_and_arg_check():
    sUsage = "<this_script> <fn_name> [fn_args] [optional_args]"

def prepare_and_set_environment():
    HOME = os.environ.get('HOME')
    HPEESOF_DIR = os.environ.get('HPEESOF_DIR')
    if not os.environ.get('AGL_EESOF_PSM'):
        AGL_EESOF_PSM = HPEESOF_DIR + '/psm'
        os.environ['AGL_EESOF_PSM'] = AGL_EESOF_PSM

    XPEDION_PLATFORM = 'linux_x86_64'
    PATH_SEP = ':'
    if sys.platform == 'win32' or sys.platform == 'cygwin':
        XPEDION_PLATFORM = 'win32_64'
        PATH_SEP = ';'

    os.environ['XPEDION_PLATFORM'] = XPEDION_PLATFORM
    #print 'XPEDION_PLATFORM', os.environ.get('XPEDION_PLATFORM')
    #print

    PATH = os.environ.get('PATH')
    os.environ['PATH'] = os.path.abspath(AGL_EESOF_PSM + '/bin') + PATH_SEP +PATH

    XPEDION = os.environ.get('PSM_DIR') or os.environ.get('XPEDION')
    if not XPEDION:
        # In the case where XPEDION was set in the environment
        print >> sys.stderr, 'PSM_DIR nor XPEDION could be found in the environment'
        return 1
    # For sake of simplicity and the change for PSM_DIR
    # put this value in the environ since it is used elsewhere
    os.environ['XPEDION'] = XPEDION
    #print 'XPEDION', XPEDION
    xpedion_bin = os.path.abspath(XPEDION + '/bin')
    

    if not os.environ.get('XPEDION_DOT_DIR'):
        if HOME:
            os.environ['XPEDION_DOT_DIR'] = os.path.abspath(HOME + '/.xpedion')
        else:
            os.environ['XPEDION_DOT_DIR'] = os.path.abspath(os.getcwd() + '/.xpedion')
    #print
    #print 'XPEDION_DOT_DIR',os.environ.get('XPEDION_DOT_DIR') 

    platform_lib = XPEDION + '/' + XPEDION_PLATFORM  + '/lib'
    so_path = platform_lib + '64:' + platform_lib

    # add so_path to LD_LIBRARY_PATH
    if XPEDION_PLATFORM == 'linux_x86_64':
        LD_LIBRARY_PATH = os.environ.get('LD_LIBRARY_PATH')
        if not LD_LIBRARY_PATH:
            os.environ['LD_LIBRARY_PATH'] = LD_LIBRARY_PATH
        elif not re.search(so_path, LD_LIBRARY_PATH):
            os.environ['LD_LIBRARY_PATH'] = os.path.abspath(XPEDION + '/' + XPEDION_PLATFORM + '/lib:' + LD_LIBRARY_PATH)
        os.environ['LD_LIBRARY_PATH'] = XPEDION + '/thirdparty/python/' + XPEDION_PLATFORM + '/lib:' + os.environ.get('LD_LIBRARY_PATH')
        os.environ['XPEDION_GCC_VERSION'] = 'x86_64'
        os.unsetenv('LD_ASSUME_KERNEL')
        #print
        #print 'LD_LIBRARY_PATH', os.environ.get('LD_LIBRARY_PATH')
        #print
        # remove compatibility environment variable which can cause memory usage to
        # climb rapidly
    if os.environ.get('LD_ASSUME_KERNEL'):
        os.unsetenv('LD_ASSUME_KERNEL')
        os.environ['XPEDION_GCC_VERSION'] = 'x86_64'
    else:
        os.environ['PATH'] = os.path.abspath(platform_lib) + PATH_SEP + os.environ.get('PATH')
    os.environ['PATH'] = os.path.abspath(XPEDION + '/thirdparty/python/' + XPEDION_PLATFORM + '/lib') + PATH_SEP + os.environ.get('PATH')
    PATH = os.environ.get('PATH')

    #if [ -z "$XPEDION_INTERNAL_DEBUG_MODE" ]; then
	    # prevent creation of core files
        #ulimit -Sc 0 1>/dev/null 2>&1
    #fi

    PYTHONHOME = XPEDION + '/thirdparty/python/' + XPEDION_PLATFORM
    os.environ[PYTHONHOME] = PYTHONHOME


    TIBURON_HOME = os.path.abspath(HPEESOF_DIR + '/tiburonda')
    os.environ['TIBURON_HOME'] = TIBURON_HOME
    os.environ['ARCH'] = XPEDION_PLATFORM

    TRUE_BIN = os.path.abspath(XPEDION + '/' + XPEDION_PLATFORM + '/bin')

    if not PATH:
        os.environ['PATH'] = TRUE_BIN + PATH_SEP + os.path.abspath(TIBURON_HOME + '/bin')
    elif not re.search(TRUE_BIN, PATH):
        #os.environ['PATH'] = TRUE_BIN + PATH_SEP + os.path.abspath(TIBURON_HOME + '/bin') + PATH_SEP + os.environ.get('PATH')
        os.environ['PATH'] = TRUE_BIN + PATH_SEP + os.environ.get('PATH')

    os.environ['PATH'] = os.path.abspath(XPEDION + '/thirdparty/python/' + XPEDION_PLATFORM + '/bin') + PATH_SEP + os.environ.get('PATH')
    #print
    #print 'PATH', os.environ.get('PATH')
    #print
    return 0

def construct_and_open_log_file():
    #usrid=`whoami`
    usrid = getpass.getuser()
    #hstid=`hostname`
    if socket.gethostname().find('.')>=0:
        hstid = socket.gethostname()
    else:
        hstid = socket.gethostbyaddr(socket.gethostname())[0]

    #prcid="$$"
    prcid = os.getpid()

    #log_fname=`mktemp -t ${usrid}_${hstid}_${prcid}.XXXXXXXX`
    log_fname = str(usrid) + '_' + str(hstid) + '_' + str(prcid)
    fd_log_fname = open(log_fname, 'w+')
    if not fd_log_fname:
        print >> sys.stderr, "Unable to open ", fd_log_fname
        sys.exit(1)

    #if [ "$?" != "0" ] ; then
    #    echo 1>&2 "$Error: $0: unable to create log file."
    #    exit 1
    #fi

    #placeholder
    #echo -n "ADS Simulation Manager (ads)" >> $log_fname
    #echo -n " " >> $log_fname
    #date >> $log_fname

    fd_log_fname.write('ADS Simulation Manager (ads) ')
    right_now = datetime.datetime.utcnow()
    fd_log_fname.write(str(right_now.year) + '_' + str(right_now.month) + '_' + str(right_now.day) + '_' + str(right_now.hour) + '_' + str(right_now.minute) + '_' + str(right_now.second) + '_' + str(right_now.microsecond))
    fd_log_fname.write('\n')
    return 0


def invoke_python_msc_utils():
    XPEDION = os.environ.get('XPEDION')
    XPEDION_PLATFORM = os.environ.get('XPEDION_PLATFORM')
    sim_mgr_python_exe = os.path.abspath(XPEDION + '/thirdparty/python/' + XPEDION_PLATFORM + '/bin/python.exe')

    M_ARGS=""
    #if [ ! -z "$PSM_M_ARGS" ] ; then
    #    M_ARGS=$PSM_M_ARGS
    #fi
    PSM_M_ARGS = os.environ.get('PSM_M_ARGS')
    if PSM_M_ARGS:
        M_ARGS = PSM_M_ARGS

    #exec mscUtils.py psm_ads "$M_ARGS" -ht ads -log $log_fname "$@"
    mscUtils_pyc_file = os.path.abspath(XPEDION + '/' + XPEDION_PLATFORM + '/python/mscUtils.pyc') 
    cmd = [sim_mgr_python_exe, mscUtils_pyc_file, 'psm_ads', M_ARGS, '-ht', 'ads']
    cmd = cmd + sys.argv[1:] ## Has to be this way to put it into one long list
    # Remove any blank strings in the cmd list
    cmd.remove('')
    str1 = ' '.join(cmd)
	
    try:
        retcode = subprocess.call(cmd)
        if retcode < 0:
            print >> sys.stderr, "psm simulation manager was terminated by signal", -retcode
        else:
            print >> sys.stderr, "psm simulation manager returned", retcode
    except OSError as e:
        print >> sys.stderr, "Execution failed for psm simulation manager:", e
    return retcode


def fMain() :

    print >> sys.stdout, "fMain() - psm"
    usage_and_arg_check()
    prepare_and_set_environment()
    construct_and_open_log_file()
    start_sim_mgr_on_windows = invoke_python_msc_utils()
    return start_sim_mgr_on_windows

if __name__ == "__main__":
    #last value is return from script
    i = fMain()

    if i != 0 :
        print >> sys.stderr, "%s returned %d" % (sys.argv[0], i)  
    sys.exit(i)



