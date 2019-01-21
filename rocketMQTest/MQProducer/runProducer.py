#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger("Producer")
import setting_MQ as settings
from jpype import *
import time
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
jvmPath = getDefaultJVMPath() or r'D:\Java\jre1.8.0_171\bin\client\jvm.dll'#### 修改文件路径为jre文件夹内jvm.dll文件
startJVM(jvmPath,settings.JVM_OPTIONS,"-Djava.class.path="+settings.JAVA_EXT_DIRS,
         "-Djava.ext.dirs=%s"%(r'..\jar'),"-Dfile.encoding=utf-8")#启动JVM,传入jar支持路径
class MQProducer(object):
    DefaultMQProducer = JPackage('com').alibaba.rocketmq.client.producer.DefaultMQProducer
    MQClientException = JPackage('com').alibaba.rocketmq.client.exception.MQClientException
    SendResult = JPackage('com').alibaba.rocketmq.client.producer.SendResult
    def __init__(self,groupName,namesrvAddr):
        """
        :param groupName    组名;
        :param namesrcAddr  host:port 地址
        :return None
        """
        self.producer = None #初始化放在init函数中
        self.groupName = groupName
        self.namesrvAddr = namesrvAddr
        self.instanceName = str(int(time.time() * 1000)) #毫秒值作为Instance name
        self.compressMsgBodyOverHowmuch = 4096 #消息压缩阀值
    def init(self):
        """批量设置一些基本项"""
        logger.info('Initializing producer ' + self.instanceName + ' ...')#日志记录实例名
        self.producer = self.DefaultMQProducer(JString(self.groupName)) # 创建实例
        self.producer.setNamesrvAddr(JString(self.namesrvAddr)) # 设置链接地址
        self.producer.setInstanceName(JString(self.instanceName)) # 设置实例名
        self.producer.setCompressMsgBodyOverHowmuch(JInt(self.compressMsgBodyOverHowmuch)) # 设置阀值
        self.producer.setVipChannelEnabled(False) #关闭VIP通道
    def start(self):
        """
            # JAVA prototype
            #    public void start() throws MQClientException {
                """
        logger.info('Starting producer ' + self.instanceName + ' ...')
        self.producer.start()
    def shutdown(self):
        """
    # JAVA prototype
    #     public void shutdown() {
        """
        logger.info('Shutting down producer ' + self.instanceName + ' ...')
        self.producer.shutdown()
    def send(self, MQMsg):
        """
    # JAVA prototype
    #    public SendResult send(Message msg, long timeout) throws MQClientException, RemotingException,
    #            MQBrokerException, InterruptedException {
    #    public void send(Message msg, SendCallback sendCallback) throws MQClientException, RemotingException,
    #            InterruptedException {
    #    public void send(Message msg, SendCallback sendCallback, long timeout) throws MQClientException,
    #            RemotingException, InterruptedException {
    #    public void sendOneway(Message msg) throws MQClientException, RemotingException, InterruptedException {
    #    public SendResult send(Message msg, MessageQueue mq) throws MQClientException, RemotingException,
    #            MQBrokerException, InterruptedException {
    #    public SendResult send(Message msg, MessageQueue mq, long timeout) throws MQClientException,
    #            RemotingException, MQBrokerException, InterruptedException {
    #    public void send(Message msg, MessageQueue mq, SendCallback sendCallback) throws MQClientException,
    #            RemotingException, InterruptedException {
    #    public void send(Message msg, MessageQueue mq, SendCallback sendCallback, long timeout)
    #            throws MQClientException, RemotingException, InterruptedException {
    #    public SendResult send(Message msg, MessageQueueSelector selector, Object arg) throws MQClientException,
    #            RemotingException, MQBrokerException, InterruptedException {
    #    public SendResult send(Message msg, MessageQueueSelector selector, Object arg, long timeout)
    #            throws MQClientException, RemotingException, MQBrokerException, InterruptedException {
    #    public void send(Message msg, MessageQueueSelector selector, Object arg, SendCallback sendCallback)
    #            throws MQClientException, RemotingException, InterruptedException {
    #    public void send(Message msg, MessageQueueSelector selector, Object arg, SendCallback sendCallback,
    #            long timeout) throws MQClientException, RemotingException, InterruptedException {
        """
        logger.debug('Producer ' + self.instanceName + ' sending message: ' + MQMsg.tostr())
        return self.producer.send(MQMsg.msg)

    def sendOneway(self, MQMsg):
        """
    # JAVA prototype
    #    public void sendOneway(Message msg) throws MQClientException, RemotingException, InterruptedException {
    #    public void sendOneway(Message msg, MessageQueue mq) throws MQClientException, RemotingException,
    #            InterruptedException {
    #    public void sendOneway(Message msg, MessageQueueSelector selector, Object arg) throws MQClientException,
    #            RemotingException, InterruptedException {
        """
        logger.debug('Producer ' + self.instanceName + ' sending one-way message: ' + MQMsg.tostr())
        return self.producer.sendOneway(MQMsg.msg)
class MQMessage(object):
    Message = JPackage('com.alibaba.rocketmq.common.message').Message
    def __init__(self,topic,tags,keys,body):
        self.topic = topic
        self.tags = tags
        self.keys = keys
        self.body = body
        self.msg = self.Message(JString(self.topic),JString(self.tags),JString(self.keys),
                             self.body.encode('utf-8'))

    def tostr(self):
        """
                Translate the object into a string
                """
        return self.topic + "::" + self.tags + "::" + self.keys + "::" + self.body

if __name__ == "__main__":

    logger.info(java.lang.System.getProperty("java.class.path"))
    logger.info(java.lang.System.getProperty("java.ext.dirs"))
    java.lang.System.out.println("Java runs correct!") 
    producer = MQProducer('DragonMdmGomeVendor_uat_test', '10.112.178.138:9876')  ####组   Host:port
    producer.init()
    producer.start()
    MQMsg = MQMessage('mdm_gome_group_vendor_uat',  #### topic
                      'mdm_gome_group_vendor_uat',  #### tag
                      'f9112a81-f4c9-4709-9ae0-d527b2347999',  #### key
                      '{"123":"郭宏杰"}')    #### 发送数据
    sendResult = producer.send(MQMsg)
    producer.shutdown()
    shutdownJVM() 
