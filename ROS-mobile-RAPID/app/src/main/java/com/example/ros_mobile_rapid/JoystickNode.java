package com.example.ros_mobile_rapid;

import org.ros.concurrent.CancellableLoop;
import java.util.Calendar;
import java.util.Date;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.NodeMain;
import org.ros.node.topic.Publisher;
import org.ros.rosjava_geometry.Vector3;

/**
 * A simple {@link Publisher} {@link NodeMain}.
 *
 * @author damonkohler@google.com (Damon Kohler)
 */
public class JoystickNode extends AbstractNodeMain {
    private final String nodeName, topicName;

    private Vector3 speeds = new Vector3(0,0,0);

    private double max_speed;
    private Publisher<geometry_msgs.Twist> publisher;
    private Boolean send = false;

    private long timer;

    private long pub_delay = 0;
    public JoystickNode(double max_speed, String Name, long delay) {
        this.max_speed = max_speed;
        this.nodeName = Name;
        this.topicName = Name;
        this.pub_delay = delay;
    }

    public double getspeed(){return this.max_speed;}

    public void setspeed(double speed){this.max_speed = speed;}

    public void editspeed(Vector3 speeds){
        this.send = true;
        this.speeds = speeds.scale(max_speed);
    }

    public long returntime(){
        return timer;
    }

    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of(nodeName + "/JoystickNode");
    }

    @Override
    public void onStart(final ConnectedNode connectedNode) {
        publisher = connectedNode.newPublisher(topicName, geometry_msgs.Twist._TYPE);
        geometry_msgs.Twist vel = publisher.newMessage();
        // This CancellableLoop will be canceled automatically when the node shuts
        // down.
        connectedNode.executeCancellableLoop(new CancellableLoop() {
            @Override
            protected void setup() {

            }
            @Override
            protected void loop() throws InterruptedException {
                if (send){
                vel.getLinear().setX(speeds.getX());
                vel.getLinear().setY(speeds.getY());
                vel.getLinear().setZ(speeds.getZ());
                publisher.publish(vel);
                send = false;
                timer = Calendar.getInstance().getTimeInMillis();
                }
                Thread.sleep(pub_delay);
            }
        });
    }
}