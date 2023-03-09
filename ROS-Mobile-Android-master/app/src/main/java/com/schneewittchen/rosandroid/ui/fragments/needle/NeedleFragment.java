package com.schneewittchen.rosandroid.ui.fragments.needle;

import android.os.Bundle;
import android.text.Editable;
import android.util.Log;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.EditorInfo;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.CompoundButton;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import com.google.android.material.switchmaterial.SwitchMaterial;
import com.google.android.material.textfield.TextInputLayout;
import com.schneewittchen.rosandroid.R;
import com.schneewittchen.rosandroid.databinding.FragmentMasterBinding;
import com.schneewittchen.rosandroid.databinding.FragmentNeedleBinding;
import com.schneewittchen.rosandroid.model.entities.widgets.BaseEntity;
import com.schneewittchen.rosandroid.model.repositories.rosRepo.node.BaseData;
import com.schneewittchen.rosandroid.ui.fragments.master.MasterFragment;
import com.schneewittchen.rosandroid.ui.fragments.viz.WidgetViewGroup;
import com.schneewittchen.rosandroid.utility.Utils;
import com.schneewittchen.rosandroid.viewmodel.MasterViewModel;
import com.schneewittchen.rosandroid.viewmodel.NeedleViewModel;

import java.util.ArrayList;


/**
 * TODO: Description
 *
 * @author Nico Studt
 * @version 1.0.2
 * @created on 10.01.20
 * @updated on 21.04.20
 * @modified by Nils Rottmann
 */
public class NeedleFragment extends Fragment implements TextView.OnEditorActionListener {

    private static final String TAG = NeedleFragment.class.getSimpleName();


    private NeedleViewModel mViewModel;
    private FragmentNeedleBinding binding;

    private TextInputLayout needleField;

    public static NeedleFragment newInstance() {
        Log.i(TAG, "New Needle Fragment");
        return new NeedleFragment();
    }


    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        binding = FragmentNeedleBinding.inflate(inflater, container, false);

        return binding.getRoot();
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);


        mViewModel = new ViewModelProvider(requireActivity()).get(NeedleViewModel.class);

        // Define Views --------------------------------------------------------------
        needleField = getView().findViewById(R.id.needle_dis_editText);

        // View model connection -------------------------------------------------------------------

        mViewModel.getNeedleDistance().observe(getViewLifecycleOwner(), needle -> {
            if (needle == null) {
                binding.needleDisEditText.getText().clear();
                return;
            }

            binding.needleDisEditText.setText();
        });
    }

    private void updateNeedleDetails() {
        // Update needle distance
        Editable needledis = binding.needleDisEditText.getText();
    }

    @Override
    public boolean onEditorAction(TextView view, int actionId, KeyEvent event) {
        switch (actionId) {
            case EditorInfo.IME_ACTION_DONE:
            case EditorInfo.IME_ACTION_NEXT:
            case EditorInfo.IME_ACTION_PREVIOUS:
                updateNeedleDetails();

                view.clearFocus();
                Utils.hideSoftKeyboard(view);

                return true;
        }

        return false;
    }
}
