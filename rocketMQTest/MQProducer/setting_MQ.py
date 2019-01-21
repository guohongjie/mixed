#!/usr/bin/python
# -*-coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='producer.log',
                    filemode='w')
RMQClientJAR = r'/home/ghj/Downloads/qwe/jar/rocketmq-client-3.5.8.jar'
JAVA_EXT_DIRS = RMQClientJAR
JVM_OPTIONS = '-mx256m'
pullMaxNums = 32
MsgBodyEncoding = 'utf-8'