package com.example.ros_mobile_rapid;

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
public class JoystickNode extends AbstractNodeMain {
    private String nodeName;

    private double x_speed;
    private double y_speed;
    private double z_speed;

    private Publisher<geometry_msgs.Twist> publisher;

    public JoystickNode( String nodeName) {
        this.nodeName = nodeName;
    }

    public void editspeed(Double x_speed, Double y_speed, Double z_speed){
        this.x_speed = x_speed;
        this.y_speed = y_speed;
        this.z_speed = z_speed;
    }

    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of(nodeName + "/JoystickNode");
    }

    @Override
    public void onStart(final ConnectedNode connectedNode) {
        publisher = connectedNode.newPublisher(nodeName+"/Twist", geometry_msgs.Twist._TYPE);
        geometry_msgs.Twist vel = publisher.newMessage();
        // This CancellableLoop will be canceled automatically when the node shuts
        // down.
        connectedNode.executeCancellableLoop(new CancellableLoop() {
            @Override
            protected void setup() {
                x_speed = 0;
                y_speed = 0;
                z_speed = 0;
            }

            @Override
            protected void loop() throws InterruptedException {
                vel.getLinear().setX(x_speed);
                vel.getLinear().setY(y_speed);
                vel.getLinear().setZ(z_speed);

                publisher.publish(vel);
                Thread.sleep(1000);
            }
        });
    }
}