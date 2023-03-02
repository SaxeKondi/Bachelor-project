package com.schneewittchen.rosandroid.widgets.sendtext;

import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;

import com.schneewittchen.rosandroid.R;
import com.schneewittchen.rosandroid.model.entities.widgets.BaseEntity;
import com.schneewittchen.rosandroid.ui.views.details.PublisherWidgetViewHolder;
import com.schneewittchen.rosandroid.utility.Utils;

import java.util.Collections;
import java.util.List;

import std_msgs.Bool;

/**
 * TODO: Description
 *
 * @author Dragos Circa
 * @version 1.0.0
 * @created on 02.11.2020
 * @updated on 18.11.2020
 * @modified by Nils Rottmann
 * @updated on 20.03.2021
 * @modified by Nico Studt
 */
public class SendtextDetailVH extends PublisherWidgetViewHolder {

    private EditText labelTextText;
    private Spinner labelTextRotationSpinner;

    private ArrayAdapter<CharSequence> rotationAdapter;


    @Override
    public void initView(View view) {
        labelTextText = view.findViewById(R.id.labelText);
        labelTextRotationSpinner = view.findViewById(R.id.labelTextRotation);

        // Init spinner
        rotationAdapter = ArrayAdapter.createFromResource(view.getContext(),
                R.array.button_rotation, android.R.layout.simple_spinner_dropdown_item);

        labelTextRotationSpinner.setAdapter(rotationAdapter);
    }

    @Override
    public void bindEntity(BaseEntity entity) {
        SendtextEntity sendtextEntity = (SendtextEntity) entity;
        int position = rotationAdapter.getPosition(Utils.numberToDegrees(sendtextEntity.rotation));

        labelTextText.setText(sendtextEntity.text);
        labelTextRotationSpinner.setSelection(position);
    }

    @Override
    public void updateEntity(BaseEntity entity) {
        int rotation = Utils.degreesToNumber(labelTextRotationSpinner.getSelectedItem().toString());

        ((SendtextEntity) entity).text = labelTextText.getText().toString();
        ((SendtextEntity) entity).rotation = rotation;
    }

    @Override
    public List<String> getTopicTypes() {
        return Collections.singletonList(Bool._TYPE);
    }


}
