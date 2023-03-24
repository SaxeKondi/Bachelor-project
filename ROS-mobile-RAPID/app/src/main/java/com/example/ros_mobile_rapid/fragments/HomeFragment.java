package com.example.ros_mobile_rapid.fragments;

import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;

import com.example.ros_mobile_rapid.JoystickNode;
import com.example.ros_mobile_rapid.R;
import com.example.ros_mobile_rapid.TextSendNode;

import org.ros.rosjava_geometry.Vector3;

import io.github.controlwear.virtual.joystick.android.JoystickView;

public class HomeFragment extends Fragment {

    private EditText NeedleDepthText;
    private Button NeedleDepthButton;

    private JoystickView JoystickRobot;
    public static TextSendNode TextSend = new TextSendNode( "NeedleDepth");
    public static JoystickNode RobotControl = new JoystickNode(0.35, "RobotControl");
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

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        JoystickRobot = getView().findViewById(R.id.joystick_robot);
        NeedleDepthText = getView().findViewById(R.id.needle_depth);
        NeedleDepthButton = getView().findViewById(R.id.needle_depth_button);
        NeedleDepthButton.setEnabled(false);

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
    }
}