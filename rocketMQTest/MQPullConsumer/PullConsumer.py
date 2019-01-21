#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import os
import logging
logger = logging.getLogger("PullConsumer")
import sys
if sys.getdefaultencoding() != 'utf8':
    reload(sys)
    sys.setdefaultencoding('utf8')
sys.path.append("..")
import settings_MQ as settings
from jpype import *
jvmPath = getDefaultJVMPath() or r'D:\Java\jre1.8.0_171\bin\client\jvm.dll'  ####值为JRE 内jvm.dll文件路径
startJVM(jvmPath, "-ea", "-Djava.ext.dirs=" + settings.JAVA_EXT_DIRS,
"-Djava.ext.dirs=%s" % (r'..\jar'),"-Dfile.encoding=utf-8")
print settings.JAVA_EXT_DIRS
logger.info(java.lang.System.getProperty("java.class.path"))
logger.info(java.lang.System.getProperty("java.ext.dirs"))

from MQPullConsumer import *
from MQMessage import MQMessage, PullStatus

import sys
if sys.getdefaultencoding() != 'utf8':
    reload(sys)
    sys.setdefaultencoding('gbk')

if __name__ == '__main__':
    list_file = os.listdir('.')
    if 'MsgBody.log' in list_file:
        os.remove('MsgBody.log')
    if 'MsgId.log' in list_file:
        os.remove('MsgId.log')

    consumer = MQPullConsumer('bh_flagshipstore_shopinfo_group_live', '10.58.50.111:9876') ####组， HOST:PORT
    consumer.init()
    consumer.start()
    consumer.fetchSubscribeMessageQueues("bh_flagshipstore_shopinfo_topic_live") ####修改topic

    while True:
        for mq in consumer.mqs:
            logger.debug("Pulling from message queue: " + str(mq.queueId))
            while True:
                try:
                    pullResult = consumer.pullBlockIfNotFound(mq, '', consumer.getMessageQueueOffset(mq), settings.pullMaxNums)
                    consumer.putMessageQueueOffset(mq, pullResult.getNextBeginOffset())
                    pullStatus = PullStatus[str(pullResult.getPullStatus())]
                    if pullStatus == PullStatus['FOUND']:
                        logger.debug('Found')
                        logger.debug(pullResult.toString())
                        msgList = pullResult.getMsgFoundList()
                        for msg in msgList:
                            logger.debug(msg.toString())
                            logger.debug("Message body: " + str(msg.body))
                            with open('MsgId.log','a+') as f:
                                print msg.getMsgId()
                                f.write(msg.getMsgId() + "\n")
                            with open('MsgBody.log','a+') as f:
                                print msg.body.__str__()
                                f.write(str(msg.body) + "\n")
                    elif pullStatus == PullStatus['NO_NEW_MSG']:
                        logger.debug('NO_NEW_MSG')
                        break
                    elif pullStatus == PullStatus['NO_MATCHED_MSG']:
                        logger.debug('NO_MATCHED_MSG')
                    elif pullStatus == PullStatus['OFFSET_ILLEGAL']:
                        logger.debug('OFFSET_ILLEGAL')
                    else:
                        logger.error('Wrong pull status: ' + str(pullStatus))
                except JavaException, ex:
                    logger.error(str(ex.javaClass()) + str(ex.message()))
                    logger.error(str(ex.stacktrace()))

    consumer.shutdown()

    shutdownJVM()
