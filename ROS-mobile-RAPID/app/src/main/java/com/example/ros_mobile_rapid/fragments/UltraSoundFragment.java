package com.example.ros_mobile_rapid.fragments;

import android.graphics.Bitmap;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.Observer;

import com.example.ros_mobile_rapid.CameraSubscriberNode;
import com.example.ros_mobile_rapid.R;

import io.github.controlwear.virtual.joystick.android.JoystickView;

public class UltraSoundFragment extends Fragment {

    private ImageView PiCameraView;
    public static CameraSubscriberNode PiCamera = new CameraSubscriberNode("PiCamera");

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_ultra_sound, container, false);
    }

    @Override
    public void onViewCreated(View view, @Nullable Bundle savedInstanceState) {
        PiCameraView = getView().findViewById(R.id.pi_camera);

        PiCamera.listen.observe(getViewLifecycleOwner(), new Observer<Bitmap>() {
            @Override
            public void onChanged(Bitmap bitmap) {
                PiCameraView.setImageBitmap(PiCamera.map);
            }
        });
    }
}