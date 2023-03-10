package com.schneewittchen.rosandroid.viewmodel;

import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MediatorLiveData;
import androidx.lifecycle.MutableLiveData;

import com.schneewittchen.rosandroid.domain.RosDomain;
import com.schneewittchen.rosandroid.model.entities.NeedleEntity;


/**
 * TODO: Description
 *
 * @author Nico Studt
 * @version 1.0.2
 * @created on 10.01.20
 * @updated on 21.04.20
 * @modified by Nils Rottmann
 */
public class NeedleViewModel extends AndroidViewModel {

    private static final String TAG = NeedleViewModel.class.getSimpleName();

    private MutableLiveData<Float> distance;


    public NeedleViewModel(@NonNull Application application) {
        super(application);
    }

    public Float setNeedleDistance(Float distance){
        return distance;
    }

    public void getNeedleDistance() {
        if (distance == null) {
            distance = new MutableLiveData<>();
        }

    }

}
