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
public class TextSendNode extends AbstractNodeMain {
    private String nodeName;

    private String text;
    private Publisher<std_msgs.String> publisher;
    private Boolean send = false;

    public TextSendNode( String nodeName) {
        this.nodeName = nodeName;
    }

    public void edittext(String input){
        this.text = input;
        this.send = true;

    }
    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of(nodeName + "/TextSendNode");
    }

    @Override
    public void onStart(final ConnectedNode connectedNode) {
         publisher = connectedNode.newPublisher(nodeName+"/String", std_msgs.String._TYPE);
         std_msgs.String str = publisher.newMessage();
        // This CancellableLoop will be canceled automatically when the node shuts
        // down.
        connectedNode.executeCancellableLoop(new CancellableLoop() {
            @Override
            protected void setup() {
            }

            @Override
            protected void loop() throws InterruptedException {
                if (send){
                    str.setData(text);
                    publisher.publish(str);
                    send = false;
                }
                Thread.sleep(1000);
            }
        });
    }
}