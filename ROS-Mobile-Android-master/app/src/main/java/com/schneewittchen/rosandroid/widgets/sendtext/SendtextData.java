package com.schneewittchen.rosandroid.widgets.sendtext;


import com.schneewittchen.rosandroid.model.entities.widgets.BaseEntity;
import com.schneewittchen.rosandroid.model.repositories.rosRepo.node.BaseData;

import org.ros.internal.message.Message;
import org.ros.node.topic.Publisher;

//import std_msgs.String;



public class SendtextData extends BaseData {

    public String data;


    public  SendtextData(String data) {
        this.data = data;
    }

    @Override
    public Message toRosMessage(Publisher<Message> publisher, BaseEntity widget) {
        std_msgs.String message = (std_msgs.String) publisher.newMessage();
        message.setData(data);
        return message;
    }
}
