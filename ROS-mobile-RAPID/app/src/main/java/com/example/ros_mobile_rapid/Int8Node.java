package com.example.ros_mobile_rapid;

import org.ros.concurrent.CancellableLoop;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.NodeMain;
import org.ros.node.topic.Publisher;

import std_msgs.Header;

/**
 * A simple {@link Publisher} {@link NodeMain}.
 *
 * @author damonkohler@google.com (Damon Kohler)
 */
public class Int8Node extends AbstractNodeMain {
    private final String nodeName, topicName;
    private Publisher<std_msgs.Int8> publisher;

    private Publisher<std_msgs.Header> header;
    private byte Int8 = 0;
    private boolean send = false;

    public Int8Node(String Name) {
        this.nodeName = Name;
        this.topicName = Name;
    }

    public void editint(byte int8){
        this.Int8 = int8;
        this.send = true;
    }
    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of(nodeName + "/Int8Node");
    }

    @Override
    public void onStart(final ConnectedNode connectedNode) {
        publisher = connectedNode.newPublisher(topicName, std_msgs.Int8._TYPE);
        std_msgs.Int8 int8 = publisher.newMessage();
        // This CancellableLoop will be canceled automatically when the node shuts
        // down.
        connectedNode.executeCancellableLoop(new CancellableLoop() {
            @Override
            protected void setup() {
            }
            @Override
            protected void loop() throws InterruptedException {
                if (send) {
                    if ((int) Int8 != 0) {
                        int8.setData(Int8);
                        publisher.publish(int8);
                    }
                    else {
                        int8.setData(Int8);
                        publisher.publish(int8);
                        send = false;
                    }
                }
                Thread.sleep(10);
            }
        });
    }
}