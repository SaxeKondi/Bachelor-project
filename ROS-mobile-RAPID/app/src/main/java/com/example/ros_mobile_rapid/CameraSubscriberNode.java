package com.example.ros_mobile_rapid;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;

import androidx.lifecycle.MutableLiveData;

import org.jboss.netty.buffer.ChannelBuffer;
import org.jboss.netty.buffer.ChannelBufferOutputStream;
import org.ros.concurrent.CancellableLoop;
import org.ros.internal.message.MessageBuffers;
import org.ros.message.MessageListener;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.NodeMain;
import org.ros.node.topic.Publisher;
import org.ros.node.topic.Subscriber;

import sensor_msgs.CompressedImage;
import std_msgs.Int8;


/**
 * A simple {@link Subscriber} {@link NodeMain}.
 *
 * @author damonkohler@google.com (Damon Kohler)
 */
public class CameraSubscriberNode extends AbstractNodeMain {
    private final String nodeName, topicName;
    private final double scaling;
    public Bitmap map;
    public Bitmap map_rotated;
    public MutableLiveData<Bitmap> mapMutableLiveData = new MutableLiveData<>();
    public MutableLiveData<Bitmap> mapRotatedMutableLiveData = new MutableLiveData<>();
    private Subscriber<sensor_msgs.CompressedImage> subscriber;

    private Publisher<sensor_msgs.CompressedImage> publisher;

    private sensor_msgs.CompressedImage subimg;

    private boolean send;
    public CameraSubscriberNode(String Name, double scaling) {
        this.nodeName = Name;
        this.topicName = Name;
        this.scaling = scaling;
    }

    @Override
    public GraphName getDefaultNodeName() {
        return GraphName.of(nodeName + "/CameraSubscriberNode");
    }

    private Bitmap convert(CompressedImage image) {
        ChannelBuffer buffer = image.getData();
        Bitmap orgBitmap = BitmapFactory.decodeByteArray(buffer.array(), buffer.arrayOffset(), buffer.readableBytes());
        return Bitmap.createScaledBitmap(orgBitmap, (int) (orgBitmap.getWidth() * this.scaling), (int) (orgBitmap.getHeight() * this.scaling), false);
    }

    private Bitmap convert_rotate(CompressedImage image) {
        ChannelBuffer buffer = image.getData();
        Bitmap orgBitmap = BitmapFactory.decodeByteArray(buffer.array(), buffer.arrayOffset(), buffer.readableBytes());

        Matrix matrix = new Matrix();

        matrix.postRotate(90);
        Bitmap rotatedBitmap = Bitmap.createBitmap(orgBitmap, 0, 0, orgBitmap.getWidth(), orgBitmap.getHeight(), matrix, true);
        return Bitmap.createScaledBitmap(rotatedBitmap, (int) (rotatedBitmap.getWidth() * 5), (int) (rotatedBitmap.getHeight() * 5), false);
    }
    @Override
    public void onStart(ConnectedNode connectedNode) {

        subscriber = connectedNode.newSubscriber(topicName, sensor_msgs.CompressedImage._TYPE);

        publisher = connectedNode.newPublisher(topicName+"pub", sensor_msgs.CompressedImage._TYPE);
        sensor_msgs.CompressedImage compimage = publisher.newMessage();
        subscriber.addMessageListener(new MessageListener<sensor_msgs.CompressedImage>() {
            @Override
            public void onNewMessage(sensor_msgs.CompressedImage image) {
                subimg = image;
//                map = convert(image);
//                mapMutableLiveData.postValue(map);
//                map_rotated = convert_rotate(image);
//                mapRotatedMutableLiveData.postValue((map_rotated));
                send = true;
            }
        });

        connectedNode.executeCancellableLoop(new CancellableLoop() {
            @Override
            protected void setup() {
            }
            @Override
            protected void loop() throws InterruptedException {
                if (send){
                    compimage.setData(subimg.getData());
                    publisher.publish(compimage);
                    send = false;
                }
                Thread.sleep(1);
            }
        });
    }
}