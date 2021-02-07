#! /usr/bin/env python
# Copyright (C) 2004 - 2017 Keysight Technologies, Inc

import os
import sys 
import subprocess
import string

HOME = os.environ.get('HOME')
#print 'HOME', HOME
XPEDION = os.environ.get('XPEDION')
#print
XPEDION_PLATFORM = os.environ.get('XPEDION_PLATFORM')

HPEESOF_DIR = os.environ.get('HPEESOF_DIR')
py_exe = HPEESOF_DIR + '/tools/' + XPEDION_PLATFORM + '/bin/python'

cmd = XPEDION + '/' + XPEDION_PLATFORM + '/bin/' + os.path.basename(sys.argv[0])
cmd_list = [cmd] + sys.argv[1:]
#print 'xpexecute cmd_list',  cmd_list
subprocess.call(cmd_list)

#exec $XPEDION_PROGRAM_WRAPPER "$XPEDION/$XPEDION_PLATFORM/bin/`basename "$0"`" "$@"

