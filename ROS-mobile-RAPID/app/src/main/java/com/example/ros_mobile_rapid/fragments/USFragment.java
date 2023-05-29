package com.example.ros_mobile_rapid.fragments;

import static com.example.ros_mobile_rapid.fragments.VideoOnlyFragment.USCamera;

import android.annotation.SuppressLint;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;

import com.example.ros_mobile_rapid.Int8Node;
import com.example.ros_mobile_rapid.R;
import com.example.ros_mobile_rapid.TextPublisherNode;

public class USFragment extends Fragment {

    private ImageView USCameraView;
    private EditText NeedleDepthAngle;
    private Button NeedleAutoStart;
    private Button NeedleRetract;
    private Button NeedleStop;
    public static TextPublisherNode NeedleDepthAngleTextSend = new TextPublisherNode( "NeedleDepthAngle");
    public static Int8Node NeedleAutoStartNode = new Int8Node("NeedleAutoStart");
    public static Int8Node NeedleRetractNode = new Int8Node("NeedleRetract");
    public static TextPublisherNode NeedleStopNode = new TextPublisherNode("tissue_type");
    private static byte AutoStart = 0, Retract = 0, Stop = 0;

    private static String blood = "b";
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_u_s, container, false);
    }

    @SuppressLint("ClickableViewAccessibility")
    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        USCameraView = getView().findViewById(R.id.us_camera_usfragment);

        NeedleDepthAngle = getView().findViewById(R.id.needle_depth_angle);

        NeedleAutoStart = getView().findViewById(R.id.needle_auto_start);

        NeedleRetract = getView().findViewById(R.id.needle_retract);

        NeedleStop = getView().findViewById(R.id.needle_stop);
        NeedleDepthAngle.addTextChangedListener(new TextWatcher() {
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                String input = s.toString();
                if(input.isEmpty() || Integer.parseInt(input) < 0) {
                    NeedleDepthAngle.setError("Please enter valid depth");
                }
                else {
                    NeedleDepthAngle.setError(null);
                    NeedleDepthAngleTextSend.edittext(NeedleDepthAngle.getText().toString());
                }
            }
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {
            }

            @Override
            public void afterTextChanged(Editable s) {
            }
        });

        NeedleAutoStart.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    NeedleAutoStartNode.editint(AutoStart);
                }
                return true;
            }
        });

        NeedleStop.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    NeedleStopNode.edittext(blood);
                }
                return true;
            }
        });

        NeedleRetract.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_DOWN) {
                    NeedleRetractNode.editint(Retract);
                }
                return true;
            }
        });
        USCamera.mapMutableLiveData.observe(getViewLifecycleOwner(), new Observer<Bitmap>() {
            @Override
            public void onChanged(Bitmap bitmap) {
                USCameraView.setImageBitmap(USCamera.map);
            }
        });
    }
}