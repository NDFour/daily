# -*- coding:utf-8 -*-
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-09-01 15:54:12
# Last Modified: 2018-09-01 17:03:19
#

import spidermonitorlib
import yeyoufang

def main():
    spidermonitorlib.setname('YEYOUFANG.COM spider')
    spidermonitorlib.start()
    yeyoufang.main()
    spidermonitorlib.finish()

main()
