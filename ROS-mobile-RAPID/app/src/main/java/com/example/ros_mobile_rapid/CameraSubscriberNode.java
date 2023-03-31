package com.example.ros_mobile_rapid;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;

import androidx.lifecycle.MutableLiveData;

import org.jboss.netty.buffer.ChannelBuffer;
import org.ros.message.MessageListener;
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
public class CameraSubscriberNode extends AbstractNodeMain {
    private final String nodeName, topicName;

    public Bitmap map;

    public MutableLiveData<Bitmap> mapMutableLiveData = new MutableLiveData<>();
    private Subscriber<sensor_msgs.CompressedImage> subscriber;

    public CameraSubscriberNode(String Name) {
        this.nodeName = Name;
        this.topicName = Name;
    }

    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of(nodeName + "/CameraSubscriberNode");
    }

    private Bitmap convert(CompressedImage image) {
        ChannelBuffer buffer = image.getData();
        return BitmapFactory.decodeByteArray(buffer.array(), buffer.arrayOffset(), buffer.readableBytes());
    }

    @Override
    public void onStart(ConnectedNode connectedNode) {

        subscriber = connectedNode.newSubscriber(topicName, sensor_msgs.CompressedImage._TYPE);
        subscriber.addMessageListener(new MessageListener<sensor_msgs.CompressedImage>() {
            @Override
            public void onNewMessage(sensor_msgs.CompressedImage image) {
                map = convert(image);
                mapMutableLiveData.postValue(map);
            }
        });
    }
}