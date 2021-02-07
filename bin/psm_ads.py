#! /usr/bin/env python
# Copyright (C) 2004 - 2017 Keysight Technologies, Inc

import os
import sys
import string
import subprocess
cmd = os.path.basename(sys.argv[0]).rstrip('.py')
cmd_list = [cmd] + sys.argv[1:]
#print
#print 'psm_ads.py cmd_list', cmd_list
subprocess.call(cmd_list)

#exec $XPEDION_PROGRAM_WRAPPER "$XPEDION/$XPEDION_PLATFORM/bin/`basename "$0"`" "$@"
