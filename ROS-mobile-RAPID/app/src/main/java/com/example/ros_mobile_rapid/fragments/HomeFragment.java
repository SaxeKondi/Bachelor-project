package com.example.ros_mobile_rapid.fragments;

import static com.example.ros_mobile_rapid.fragments.VideoOnlyFragment.PiCamera;
import static com.example.ros_mobile_rapid.fragments.VideoOnlyFragment.USCamera;

import android.annotation.SuppressLint;
import android.graphics.Bitmap;
import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;

import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import com.example.ros_mobile_rapid.JoystickNode;
import com.example.ros_mobile_rapid.R;
import com.example.ros_mobile_rapid.RotationNode;
import com.example.ros_mobile_rapid.TextPublisherNode;

import org.ros.rosjava_geometry.Vector3;

import io.github.controlwear.virtual.joystick.android.JoystickView;

public class HomeFragment extends Fragment {
    private EditText NeedleDepthText;
    private Button NeedleDepthButton;
    private ImageView PiCameraView;
    private ImageView USCameraView;
    private static byte Rotate_pos = 1, Rotate_neg = -1, Rotate_default = 0;
    private Button Roll_pos;
    private Button Roll_neg;
    private Button Pitch_pos;
    private Button Pitch_neg;
    private Button Yaw_pos;
    private Button Yaw_neg;

    private Button Z_pos;
    private Button Z_neg;
    private JoystickView JoystickRobot;
    private JoystickView JoystickCamera;
    public static TextPublisherNode TextSend = new TextPublisherNode( "NeedleDepth");
    public static JoystickNode RobotControl = new JoystickNode(0.35, "RobotControl");
    public static JoystickNode CameraControl = new JoystickNode(1, "CameraControl");
    public static RotationNode RollControl = new RotationNode("Roll");
    public static RotationNode PitchControl = new RotationNode("Pitch");
    public static RotationNode YawControl = new RotationNode("Yaw");
    public static RotationNode ZControl = new RotationNode("ZAxis");
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

        Z_pos = getView().findViewById(R.id.z_pos);
        Z_neg = getView().findViewById(R.id.z_neg);

        NeedleDepthText = getView().findViewById(R.id.needle_depth);

        NeedleDepthButton = getView().findViewById(R.id.needle_depth_button);
        NeedleDepthButton.setEnabled(false);

        Roll_pos = getView().findViewById(R.id.roll_pos);
        Roll_neg = getView().findViewById(R.id.roll_neg);

        Pitch_pos = getView().findViewById(R.id.pitch_pos);
        Pitch_neg = getView().findViewById(R.id.pitch_neg);

        Yaw_pos = getView().findViewById(R.id.yaw_pos);
        Yaw_neg = getView().findViewById(R.id.yaw_neg);

        PiCameraView = getView().findViewById(R.id.pi_cam);
        USCameraView = getView().findViewById(R.id.us_cam);




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
                RobotVector = new Vector3(str*Math.cos(angle),str*Math.sin(angle),0);
                RobotControl.editspeed(RobotVector);
            }
        },10);

        JoystickCamera.setOnMoveListener(new JoystickView.OnMoveListener() {
            @Override
            public void onMove(int angle, int strength) {
                double str = (double) strength / 100;
                CameraVector = new Vector3(str*Math.cos(angle),str*Math.sin(angle),0);
                CameraControl.editspeed(CameraVector);
            }
        },10);
        NeedleDepthText.addTextChangedListener(new TextWatcher() {
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                String input = s.toString();
                if(input.isEmpty() || Integer.parseInt(input) < 0) {
                    NeedleDepthText.setError("Please enter valid depth");
                    NeedleDepthButton.setEnabled(false);
                }
                else {
                    NeedleDepthText.setError(null);
                    NeedleDepthButton.setEnabled(true);
                }
            }
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void afterTextChanged(Editable s) {
            }
        });
        NeedleDepthButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                TextSend.edittext(NeedleDepthText.getText().toString());
            }
        });

        Z_pos.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Z_neg.setEnabled(false);
                    Z_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_500));
                    Z_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    ZControl.editrotation(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Z_neg.setEnabled(true);
                    Z_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Z_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    ZControl.editrotation(Rotate_default);
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
                    ZControl.editrotation(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Z_pos.setEnabled(true);
                    Z_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Z_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    ZControl.editrotation(Rotate_default);
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
                    RollControl.editrotation(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Roll_neg.setEnabled(true);
                    Roll_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Roll_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    RollControl.editrotation(Rotate_default);
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
                    RollControl.editrotation(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Roll_pos.setEnabled(true);
                    Roll_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Roll_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    RollControl.editrotation(Rotate_default);
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
                    PitchControl.editrotation(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Pitch_neg.setEnabled(true);
                    Pitch_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Pitch_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    PitchControl.editrotation(Rotate_default);
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
                    PitchControl.editrotation(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Pitch_pos.setEnabled(true);
                    Pitch_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Pitch_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    PitchControl.editrotation(Rotate_default);
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
                    YawControl.editrotation(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Yaw_neg.setEnabled(true);
                    Yaw_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Yaw_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    YawControl.editrotation(Rotate_default);
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
                    YawControl.editrotation(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Yaw_pos.setEnabled(true);
                    Yaw_pos.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    Yaw_neg.setBackgroundColor(getResources().getColor(R.color.blue_main_200));
                    YawControl.editrotation(Rotate_default);
                }
                return true;
            }
        });

    }
}