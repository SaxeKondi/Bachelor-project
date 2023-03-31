package com.example.ros_mobile_rapid.fragments;

import android.graphics.Bitmap;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;

import com.example.ros_mobile_rapid.CameraSubscriberNode;
import com.example.ros_mobile_rapid.R;

public class VideoOnlyFragment extends Fragment {

    private ImageView PiCameraView;
    private ImageView USCameraView;
    public static CameraSubscriberNode PiCamera = new CameraSubscriberNode("PiCamera");
    public static CameraSubscriberNode USCamera = new CameraSubscriberNode("USCamera");

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_video_only, container, false);
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        PiCameraView = getView().findViewById(R.id.pi_camera);
        USCameraView = getView().findViewById(R.id.us_camera);

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
    }
}