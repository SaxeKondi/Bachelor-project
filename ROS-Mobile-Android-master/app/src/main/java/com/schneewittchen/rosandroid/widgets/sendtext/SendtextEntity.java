package com.schneewittchen.rosandroid.widgets.sendtext;

import com.schneewittchen.rosandroid.model.entities.widgets.PublisherWidgetEntity;
import com.schneewittchen.rosandroid.model.repositories.rosRepo.message.Topic;


/**
 * TODO: Description
 *
 * @author Dragos Circa
 * @version 1.0.0
 * @created on 02.11.2020
 * @updated on 18.11.2020
 * @modified by Nils Rottmann
 * @updated on 01.04.2021
 * @modified by Nico Studt
 */
public class SendtextEntity extends PublisherWidgetEntity {

    public String text;
    public int rotation;

    public SendtextEntity() {
        this.width = 3;
        this.height = 1;
        this.topic = new Topic("dis", std_msgs.String._TYPE);
        this.text = "Input";
        this.rotation = 0;
    }
}
