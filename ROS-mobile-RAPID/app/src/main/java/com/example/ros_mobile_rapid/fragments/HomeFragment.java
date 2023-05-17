package com.example.ros_mobile_rapid.fragments;

import static com.example.ros_mobile_rapid.fragments.VideoOnlyFragment.PiCamera;
import static com.example.ros_mobile_rapid.fragments.VideoOnlyFragment.USCamera;

import android.annotation.SuppressLint;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;

import com.example.ros_mobile_rapid.Int8Node;
import com.example.ros_mobile_rapid.JoystickNode;
import com.example.ros_mobile_rapid.LatencyTestSubNode;
import com.example.ros_mobile_rapid.R;

import org.ros.message.Duration;
import org.ros.rosjava_geometry.Vector3;

import io.github.controlwear.virtual.joystick.android.JoystickView;

public class HomeFragment extends Fragment {
    private ImageView PiCameraView;
    private ImageView USCameraView;
    private static final byte Rotate_pos = 1, Rotate_neg = -1, Rotate_default = 0;
    private Button Roll_pos;
    private Button Roll_neg;
    private Button Pitch_pos;
    private Button Pitch_neg;
    private Button Yaw_pos;
    private Button Yaw_neg;
    private Button Z_pos;
    private Button Z_neg;
    private Button Z_cal;
    private Button Lat_test;
    private JoystickView JoystickRobot;
    private JoystickView JoystickCamera;
    public static JoystickNode RobotControl = new JoystickNode(0.05, "RobotControl", 10);
    public static LatencyTestSubNode LatencyTest = new LatencyTestSubNode("Latency");
    public static JoystickNode CameraControl = new JoystickNode(1, "CameraControl", 10);
    public static Int8Node RollControl = new Int8Node("Roll");
    public static Int8Node PitchControl = new Int8Node("Pitch");
    public static Int8Node YawControl = new Int8Node("Yaw");
    public static Int8Node ZControl = new Int8Node("ZAxis");
    public static Int8Node ZCal = new Int8Node("ZCal");
    private Vector3 RobotVector = new Vector3(0,0,0);
    private Vector3 CameraVector = new Vector3(0,0,0);
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_home, container, false);
    }

    @SuppressLint("ClickableViewAccessibility")
    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {

        JoystickRobot = getView().findViewById(R.id.joystick_robot);
        JoystickCamera = getView().findViewById(R.id.joystick_camera);

        Lat_test = getView().findViewById(R.id.lat_test);

        Z_pos = getView().findViewById(R.id.z_pos);
        Z_neg = getView().findViewById(R.id.z_neg);
        Z_pos.setEnabled(false);
        Z_neg.setEnabled(false);
        Z_neg.setVisibility(View.GONE);
        Z_pos.setVisibility(View.GONE);
        Z_cal = getView().findViewById(R.id.z_cal);

        Roll_pos = getView().findViewById(R.id.roll_pos);
        Roll_neg = getView().findViewById(R.id.roll_neg);

        Pitch_pos = getView().findViewById(R.id.pitch_pos);
        Pitch_neg = getView().findViewById(R.id.pitch_neg);

        Yaw_pos = getView().findViewById(R.id.yaw_pos);
        Yaw_neg = getView().findViewById(R.id.yaw_neg);

        PiCameraView = getView().findViewById(R.id.pi_cam);
        USCameraView = getView().findViewById(R.id.us_cam);

//        Lat_test.setVisibility(View.GONE);
        Lat_test.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    RobotControl.editspeed(new Vector3(1,1,0));
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                }
                return true;
            }
        });

        LatencyTest.TimeMutableLiveData.observe(getViewLifecycleOwner(), new Observer<Long>() {
            @Override
            public void onChanged(Long dur) {
                Long temp = dur/2;
                Log.d("myTag", temp.toString());
            }
        });
        PiCamera.mapMutableLiveData.observe(getViewLifecycleOwner(), new Observer<Bitmap>() {
            @Override
            public void onChanged(Bitmap bitmap) {
                PiCameraView.setImageBitmap(PiCamera.map);
            }
        });
        USCamera.mapMutableLiveData.observe(getViewLifecycleOwner(), new Observer<Bitmap>() {
            @Override
            public void onChanged(Bitmap bitmap) {
                USCameraView.setImageBitmap(USCamera.map);
            }
        });
        JoystickRobot.setOnMoveListener(new JoystickView.OnMoveListener() {
            @Override
            public void onMove(int angle, int strength) {
                double str = (double) strength / 100;
                RobotVector = new Vector3(str*Math.cos((angle*Math.PI) / 180),str*Math.sin((angle*Math.PI) / 180),0);
                RobotControl.editspeed(RobotVector);
            }
        },10);

        JoystickCamera.setOnMoveListener(new JoystickView.OnMoveListener() {
            @Override
            public void onMove(int angle, int strength) {
                double str = (double) strength / 100;
                CameraVector = new Vector3(str*Math.cos((angle*Math.PI) / 180),str*Math.sin((angle*Math.PI) / 180),0);
                CameraControl.editspeed(CameraVector);
            }
        },10);
        Z_cal.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Z_cal.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    ZCal.editint(Rotate_default);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Z_neg.setEnabled(true);
                    Z_pos.setEnabled(true);
                    Z_cal.setEnabled(false);
                    Z_cal.setVisibility(View.GONE);
                    Z_neg.setVisibility(View.VISIBLE);
                    Z_pos.setVisibility(View.VISIBLE);
                }
                return true;
            }
        });
        Z_pos.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Z_neg.setEnabled(false);
                    Z_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    Z_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    ZControl.editint(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Z_neg.setEnabled(true);
                    Z_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Z_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    ZControl.editint(Rotate_default);
                }
                return true;
            }
        });

        Z_neg.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Z_pos.setEnabled(false);
                    Z_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    Z_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    ZControl.editint(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Z_pos.setEnabled(true);
                    Z_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Z_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    ZControl.editint(Rotate_default);
                }
                return true;
            }
        });
        Roll_pos.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Roll_neg.setEnabled(false);
                    Roll_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    Roll_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    RollControl.editint(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Roll_neg.setEnabled(true);
                    Roll_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Roll_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    RollControl.editint(Rotate_default);
                }
                return true;
            }
        });

        Roll_neg.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Roll_pos.setEnabled(false);
                    Roll_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    Roll_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    RollControl.editint(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Roll_pos.setEnabled(true);
                    Roll_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Roll_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    RollControl.editint(Rotate_default);
                }
                return true;
            }
        });

        Pitch_pos.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Pitch_neg.setEnabled(false);
                    Pitch_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    Pitch_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    PitchControl.editint(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Pitch_neg.setEnabled(true);
                    Pitch_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Pitch_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    PitchControl.editint(Rotate_default);
                }
                return true;
            }
        });

        Pitch_neg.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Pitch_pos.setEnabled(false);
                    Pitch_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Pitch_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    PitchControl.editint(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Pitch_pos.setEnabled(true);
                    Pitch_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Pitch_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    PitchControl.editint(Rotate_default);
                }
                return true;
            }
        });
        Yaw_pos.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Yaw_neg.setEnabled(false);
                    Yaw_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    Yaw_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    YawControl.editint(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Yaw_neg.setEnabled(true);
                    Yaw_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Yaw_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    YawControl.editint(Rotate_default);
                }
                return true;
            }
        });

        Yaw_neg.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Yaw_pos.setEnabled(false);
                    Yaw_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Yaw_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    YawControl.editint(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Yaw_pos.setEnabled(true);
                    Yaw_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Yaw_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    YawControl.editint(Rotate_default);
                }
                return true;
            }
        });

    }
}