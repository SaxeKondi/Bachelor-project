package com.example.ros_mobile_rapid;

import android.content.Context;

import org.ros.concurrent.CancellableLoop;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.NodeMain;
import org.ros.node.topic.Publisher;

/**
 * A simple {@link Publisher} {@link NodeMain}.
 *
 * @author damonkohler@google.com (Damon Kohler)
 */
public class RotationNode extends AbstractNodeMain {
    private final String nodeName, topicName;

    private Publisher<std_msgs.Int8> publisher;
    private byte rotation = 0;
    private boolean send = false;

    public RotationNode( String Name) {
        this.nodeName = Name;
        this.topicName = Name;
    }

    public void editrotation(byte rotation){
        this.rotation = rotation;
        this.send = true;

    }
    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of(nodeName + "/RotationNode");
    }

    @Override
    public void onStart(final ConnectedNode connectedNode) {
        publisher = connectedNode.newPublisher(topicName, std_msgs.Int8._TYPE);
        std_msgs.Int8 rot = publisher.newMessage();
        // This CancellableLoop will be canceled automatically when the node shuts
        // down.
        connectedNode.executeCancellableLoop(new CancellableLoop() {
            @Override
            protected void setup() {
            }

            @Override
            protected void loop() throws InterruptedException {
                if (send){
                    rot.setData(rotation);
                    publisher.publish(rot);
                    send = false;
                }
                Thread.sleep(100);
            }
        });
    }
}