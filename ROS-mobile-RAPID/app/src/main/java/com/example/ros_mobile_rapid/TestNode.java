package com.example.ros_mobile_rapid;

import android.content.Context;
import android.util.Log;

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
public class TestNode extends AbstractNodeMain {

    private final Context context;
    private String nodeName;
    private Publisher<std_msgs.String> publisher;

    public TestNode(Context context, String nodeName) {
        this.context = context;
        //this.previewView = previewView;
        this.nodeName = nodeName;
    }

    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of(nodeName + "/TestNode");
    }

    @Override
    public void onStart(final ConnectedNode connectedNode) {
         publisher = connectedNode.newPublisher(nodeName+"/String", std_msgs.String._TYPE);
         std_msgs.String str = publisher.newMessage();
        // This CancellableLoop will be canceled automatically when the node shuts
        // down.
        connectedNode.executeCancellableLoop(new CancellableLoop() {
            private int sequenceNumber;

            @Override
            protected void setup() {
                sequenceNumber = 0;
            }

            @Override
            protected void loop() throws InterruptedException {

                str.setData("Hello world! " + sequenceNumber);
                publisher.publish(str);
                sequenceNumber++;
                Thread.sleep(1000);
            }
        });
    }
}