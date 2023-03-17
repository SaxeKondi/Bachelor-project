package com.example.ros_mobile_rapid;

import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.IBinder;
import android.text.TextUtils;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;

import org.ros.address.InetAddressFactory;
import org.ros.android.MasterChooser;
import org.ros.android.NodeMainExecutorService;
import org.ros.exception.RosRuntimeException;
import org.ros.node.NodeConfiguration;
import org.ros.node.NodeMainExecutor;

import java.net.NetworkInterface;
import java.net.SocketException;
import java.net.URI;
import java.net.URISyntaxException;

public class MainActivity extends AppCompatActivity {
    private static final int MASTER_CHOOSER_REQUEST_CODE = 0;
    private ServiceConnection nodeMainExecutorServiceConnection;
    private NodeMainExecutorService nodeMainExecutorService;
    private MutableLiveData<NodeMainExecutor> nodeMainExecutorMutableLiveData = new MutableLiveData<>();
    private MutableLiveData<NodeConfiguration> nodeConfigurationMutableLiveData= new MutableLiveData<>();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Intent intent = getIntent();
        String masterUri = intent.getStringExtra(CustomMasterChooser.MASTER_URI);

        URI customUri = null;
        try {
            customUri = new URI(masterUri);
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
        nodeMainExecutorServiceConnection = new NodeMainExecutorServiceConnection(customUri);

    }

    @Override
    protected void onStart() {
        super.onStart();

        final Intent intent = new Intent(this, NodeMainExecutorService.class);

        intent.setAction(NodeMainExecutorService.ACTION_START);
        intent.putExtra(NodeMainExecutorService.EXTRA_NOTIFICATION_TICKER, getString(R.string.app_name));
        intent.putExtra(NodeMainExecutorService.EXTRA_NOTIFICATION_TITLE, getString(R.string.app_name));
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent);
        } else {
            startService(intent);
        }
        if (!bindService(intent, nodeMainExecutorServiceConnection, BIND_AUTO_CREATE)) {
            Toast.makeText(this, "Failed to bind NodeMainExecutorService.", Toast.LENGTH_LONG).show();
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        unbindService(nodeMainExecutorServiceConnection);
        final Intent intent = new Intent(this, NodeMainExecutorService.class);
        stopService(intent);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK) {
            if (requestCode == MASTER_CHOOSER_REQUEST_CODE) {
                final String host;
                final String networkInterfaceName = data.getStringExtra("ROS_MASTER_NETWORK_INTERFACE");
                // Handles the default selection and prevents possible errors
                if (TextUtils.isEmpty(networkInterfaceName)) {
                    host = InetAddressFactory.newNonLoopback().getHostAddress();
                } else {
                    try {
                        final NetworkInterface networkInterface = NetworkInterface.getByName(networkInterfaceName);
                        host = InetAddressFactory.newNonLoopbackForNetworkInterface(networkInterface).getHostAddress();
                    } catch (final SocketException e) {
                        throw new RosRuntimeException(e);
                    }
                }
                nodeMainExecutorService.setRosHostname(host);
                if (data.getBooleanExtra("ROS_MASTER_CREATE_NEW", false)) {
                    nodeMainExecutorService.startMaster(data.getBooleanExtra("ROS_MASTER_PRIVATE", true));
                } else {
                    final URI uri;
                    try {
                        uri = new URI(data.getStringExtra("ROS_MASTER_URI"));
                    } catch (final URISyntaxException e) {
                        throw new RosRuntimeException(e);
                    }
                    nodeMainExecutorService.setMasterUri(uri);
                }
                // Run init() in a new thread as a convenience since it often requires network access.
                new Thread(() -> init(nodeMainExecutorService)).start();
            } else {
                // Without a master URI configured, we are in an unusable state.
                nodeMainExecutorService.forceShutdown();
            }
        }
    }

    /** Gets the main executor. */
    public LiveData<NodeMainExecutor> getNodeMainExec() {
        return nodeMainExecutorMutableLiveData;
    }

    /** Gets the node configuration. */
    public LiveData<NodeConfiguration> getNodeConfig() {
        return nodeConfigurationMutableLiveData;
    }

    protected void init(NodeMainExecutor nodeMainExecutor) {

        //Network configuration with ROS master
        final NodeConfiguration nodeConfiguration = NodeConfiguration.newPublic(
                InetAddressFactory.newNonLoopback().getHostAddress()
        );
        nodeConfiguration.setMasterUri(nodeMainExecutorService.getMasterUri());

        Handler mainHandler = new Handler(getMainLooper());
        mainHandler.post(()-> {
            this.nodeMainExecutorMutableLiveData.setValue(nodeMainExecutor);
            this.nodeConfigurationMutableLiveData.setValue(nodeConfiguration);
        });
        // Run nodes: http://rosjava.github.io/rosjava_core/0.0.0/javadoc/org/ros/node/NodeMainExecutor.html
    }

    @SuppressWarnings("NonStaticInnerClassInSecureContext")
    private final class NodeMainExecutorServiceConnection implements ServiceConnection {

        private final URI customMasterUri;

        public NodeMainExecutorServiceConnection(final URI customUri) {
            customMasterUri = customUri;
        }

        @Override
        public void onServiceConnected(final ComponentName name, final IBinder binder) {
            nodeMainExecutorService = ((NodeMainExecutorService.LocalBinder) binder).getService();

            if (customMasterUri != null) {
                nodeMainExecutorService.setMasterUri(customMasterUri);
                final String host = InetAddressFactory.newNonLoopback().getHostAddress();
                nodeMainExecutorService.setRosHostname(host);
            }
            nodeMainExecutorService.addListener(executorService -> {
                // We may have added multiple shutdown listeners and we only want to
                // call finish() once.
                if (!isFinishing()) {
                    finish();
                }
            });
            if (nodeMainExecutorService.getMasterUri() == null) {

                startActivityForResult(
                        new Intent(MainActivity.this, MasterChooser.class),
                        MASTER_CHOOSER_REQUEST_CODE
                );

            } else {
                init(nodeMainExecutorService);
            }
        }

        @Override
        public void onServiceDisconnected(final ComponentName name) {
            Toast.makeText(MainActivity.this, "Service disconnected", Toast.LENGTH_LONG).show();
        }
    }
}

