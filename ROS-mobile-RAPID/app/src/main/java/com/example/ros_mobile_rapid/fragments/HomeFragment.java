package com.example.ros_mobile_rapid.fragments;

import android.annotation.SuppressLint;
import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;

import com.example.ros_mobile_rapid.JoystickNode;
import com.example.ros_mobile_rapid.R;
import com.example.ros_mobile_rapid.RotationNode;
import com.example.ros_mobile_rapid.TextPublisherNode;

import org.ros.rosjava_geometry.Vector3;

import io.github.controlwear.virtual.joystick.android.JoystickView;

public class HomeFragment extends Fragment {
    private EditText NeedleDepthText;
    private Button NeedleDepthButton;

    private static byte Rotate_pos = 1, Rotate_neg = -1, Rotate_default = 0;

    private Button Roll_pos;

    private Button Roll_neg;

    private Button Yaw_pos;

    private Button Yaw_neg;
    private JoystickView JoystickRobot;
    public static TextPublisherNode TextSend = new TextPublisherNode( "NeedleDepth");
    public static JoystickNode RobotControl = new JoystickNode(0.35, "RobotControl");

    public static RotationNode RollControl = new RotationNode("Roll");

    public static RotationNode YawControl = new RotationNode("Yaw");

    private Vector3 RobotVector = new Vector3(0,0,0);

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

        NeedleDepthText = getView().findViewById(R.id.needle_depth);

        NeedleDepthButton = getView().findViewById(R.id.needle_depth_button);
        NeedleDepthButton.setEnabled(false);

        Yaw_pos = getView().findViewById(R.id.yaw_pos);
        Yaw_neg = getView().findViewById(R.id.yaw_neg);

        Roll_pos = getView().findViewById(R.id.roll_pos);
        Roll_neg = getView().findViewById(R.id.roll_neg);


        JoystickRobot.setOnMoveListener(new JoystickView.OnMoveListener() {
            @Override
            public void onMove(int angle, int strength) {
                double str = (double) strength / 100;
                RobotVector = new Vector3(str*Math.cos(angle),str*Math.sin(angle),0);
                RobotControl.editspeed(RobotVector);
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

        Yaw_pos.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Yaw_neg.setEnabled(false);
                    YawControl.editrotation(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    YawControl.editrotation(Rotate_default);
                    Yaw_neg.setEnabled(true);
                }
                return true;
            }
        });

        Yaw_neg.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Yaw_pos.setEnabled(false);
                    YawControl.editrotation(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Yaw_pos.setEnabled(true);
                    YawControl.editrotation(Rotate_default);
                }
                return true;
            }
        });

        Roll_pos.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    Roll_neg.setEnabled(false);
                    RollControl.editrotation(Rotate_pos);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Roll_neg.setEnabled(true);
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
                    RollControl.editrotation(Rotate_neg);
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    Roll_pos.setEnabled(true);
                    RollControl.editrotation(Rotate_default);
                }
                return true;
            }
        });

    }
}