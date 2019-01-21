#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import logging

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='rmq.log',  
                    filemode='w')

RMQClientJAR = r'..\jar\rocketmq-client-3.1.3.jar'
JAVA_EXT_DIRS = RMQClientJAR

#startJVM中的options参数不能包含空格！只能一项一项填写
#JVM_OPTIONS = '-Xms32m -Xmx256m -mx256m'
JVM_OPTIONS = '-mx256m'

pullMaxNums = 32
MsgBodyEncoding = 'utf-8'
