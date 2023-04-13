package com.example.ros_mobile_rapid.fragments;

import static com.example.ros_mobile_rapid.fragments.VideoOnlyFragment.USCamera;

import android.content.pm.ActivityInfo;
import android.graphics.Bitmap;
import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;

import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import com.example.ros_mobile_rapid.R;
import com.example.ros_mobile_rapid.Int8Node;
import com.example.ros_mobile_rapid.TextPublisherNode;

public class USFragment extends Fragment {

    private ImageView USCameraView;
    private EditText NeedleDepthAngle;
    private Button NeedleAutoStart;
    public static TextPublisherNode NeedleDepthAngleTextSend = new TextPublisherNode( "NeedleDepthAngle");
    public static Int8Node NeedleAutoStartNode = new Int8Node("NeedleAutoStart");
    private static byte AutoStart = 1, AutoStop = -1, Auto_default = 0;

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

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        USCameraView = getView().findViewById(R.id.us_camera_usfragment);

        NeedleDepthAngle = getView().findViewById(R.id.needle_depth_angle);

        NeedleAutoStart = getView().findViewById(R.id.needle_auto_start);

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

        NeedleAutoStart.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                NeedleAutoStartNode.editint(AutoStart);
            }
        });

        USCamera.mapMutableLiveData.observe(getViewLifecycleOwner(), new Observer<Bitmap>() {
            @Override
            public void onChanged(Bitmap bitmap) {
                USCameraView.setImageBitmap(USCamera.map_rotated);
            }
        });
    }
}