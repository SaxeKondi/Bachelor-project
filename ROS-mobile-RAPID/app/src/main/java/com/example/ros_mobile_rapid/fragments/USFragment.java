package com.example.ros_mobile_rapid.fragments;

import static com.example.ros_mobile_rapid.fragments.VideoOnlyFragment.USCamera;

import android.graphics.Bitmap;
import android.os.Bundle;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;

import com.example.ros_mobile_rapid.CameraSubscriberNode;
import com.example.ros_mobile_rapid.R;

public class USFragment extends Fragment {

    private ImageView USCameraView;

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

        USCamera.mapMutableLiveData.observe(getViewLifecycleOwner(), new Observer<Bitmap>() {
            @Override
            public void onChanged(Bitmap bitmap) {
                USCameraView.setImageBitmap(USCamera.map_rotated);
            }
        });
    }
}