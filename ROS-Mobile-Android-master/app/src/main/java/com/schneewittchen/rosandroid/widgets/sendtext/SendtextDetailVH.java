package com.schneewittchen.rosandroid.widgets.sendtext;

import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;

import com.schneewittchen.rosandroid.R;
import com.schneewittchen.rosandroid.model.entities.widgets.BaseEntity;
import com.schneewittchen.rosandroid.ui.views.details.PublisherWidgetViewHolder;
import com.schneewittchen.rosandroid.utility.Utils;
import com.schneewittchen.rosandroid.widgets.button.ButtonEntity;

import java.util.Collections;
import java.util.List;



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

    private EditText sendTextText;
    private Spinner sendTextRotationSpinner;
    private ArrayAdapter<CharSequence> rotationAdapter;


    @Override
    public void initView(View view) {
        sendTextText = view.findViewById(R.id.sendTextTypeText);
        sendTextRotationSpinner = view.findViewById(R.id.sendTextTypeRotation);

        // Init spinner
        rotationAdapter = ArrayAdapter.createFromResource(view.getContext(),
                R.array.sendtext_rotation, android.R.layout.simple_spinner_dropdown_item);

        sendTextRotationSpinner.setAdapter(rotationAdapter);
    }

    @Override
    public void bindEntity(BaseEntity entity) {
        SendtextEntity sendtextEntity = (SendtextEntity) entity;
        sendTextText.setText(sendtextEntity.text);

        String degrees = Utils.numberToDegrees(sendtextEntity.rotation);
        sendTextRotationSpinner.setSelection(rotationAdapter.getPosition(degrees));
    }

    @Override
    protected void updateEntity(BaseEntity entity) {
        SendtextEntity sendtextEntity = (SendtextEntity) entity;

        sendtextEntity.text = sendTextText.getText().toString();
        String degrees = sendTextRotationSpinner.getSelectedItem().toString();
        sendtextEntity.rotation = Utils.degreesToNumber(degrees);
    }

    @Override
    public List<String> getTopicTypes() {
        return Collections.singletonList(std_msgs.String._TYPE);
    }


}
