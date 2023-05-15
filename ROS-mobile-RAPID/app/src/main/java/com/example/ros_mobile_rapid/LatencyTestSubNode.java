package com.example.ros_mobile_rapid;

import static com.example.ros_mobile_rapid.fragments.HomeFragment.RobotControl;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;

import androidx.lifecycle.MutableLiveData;

import org.jboss.netty.buffer.ChannelBuffer;
import org.ros.message.Duration;
import org.ros.message.MessageListener;
import java.util.Calendar;
import java.util.Date;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.NodeMain;
import org.ros.node.topic.Subscriber;
import sensor_msgs.CompressedImage;


/**
 * A simple {@link Subscriber} {@link NodeMain}.
 *
 * @author damonkohler@google.com (Damon Kohler)
 */
public class LatencyTestSubNode extends AbstractNodeMain {
    private final String nodeName, topicName;
    private long timer;
    private long timer_robot;
    public MutableLiveData<Long> TimeMutableLiveData = new MutableLiveData<>();

    private Subscriber<geometry_msgs.Twist> subscriber;

    public LatencyTestSubNode(String Name) {
        this.nodeName = Name;
        this.topicName = Name;
    }

    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of(nodeName + "/LatencyTestSubNode");
    }


    @Override
    public void onStart(ConnectedNode connectedNode) {

        subscriber = connectedNode.newSubscriber(topicName, geometry_msgs.Twist._TYPE);
        subscriber.addMessageListener(new MessageListener<geometry_msgs.Twist>() {
            @Override
            public void onNewMessage(geometry_msgs.Twist twist) {
                timer = Calendar.getInstance().getTimeInMillis();
                timer_robot = RobotControl.returntime();
                TimeMutableLiveData.postValue(timer - timer_robot);
            }
        });
    }
}