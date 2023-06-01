package com.example.ros_mobile_rapid;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.viewpager2.adapter.FragmentStateAdapter;

import com.example.ros_mobile_rapid.fragments.HomeFragment;
import com.example.ros_mobile_rapid.fragments.USFragment;
import com.example.ros_mobile_rapid.fragments.VideoOnlyFragment;

public class MyViewPageAdapter extends FragmentStateAdapter {

    public MyViewPageAdapter(@NonNull FragmentActivity fragmentActivity) {
        super(fragmentActivity);
    }

    @NonNull
    @Override
    public Fragment createFragment(int position) {
        switch (position){
            case 0:
                return new HomeFragment();
            case 1:
                return new VideoOnlyFragment();
            case 2:
                return new USFragment();
            default:
                return new HomeFragment();
        }
    }

    @Override
    public int getItemCount() {
        return 3;
    }
}
