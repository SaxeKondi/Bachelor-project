package com.schneewittchen.rosandroid.widgets.sendtext;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.text.Layout;
import android.text.StaticLayout;
import android.text.TextPaint;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.widget.EditText;

import com.schneewittchen.rosandroid.R;
import com.schneewittchen.rosandroid.ui.views.widgets.PublisherWidgetView;
import com.schneewittchen.rosandroid.widgets.button.ButtonEntity;

import javax.annotation.Nullable;

/**
 * TODO: Description
 *
 * @author Dragos Circa
 * @version 1.0.0
 * @created on 02.11.2020
 * @updated on 18.11.2020
 * @modified by Nils Rottmann
 */

public class SendtextView extends PublisherWidgetView {

    public static final String TAG = SendtextView.class.getSimpleName();

    TextPaint textPaint;
    Paint backgroundPaint;
    StaticLayout staticLayout;

    String data;

    public SendtextView(Context context) {
        super(context);
        init();
    }

    public SendtextView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        init();
    }

    private void init() {
        backgroundPaint = new Paint();
        backgroundPaint.setColor(getResources().getColor(R.color.colorPrimary));
        backgroundPaint.setStyle(Paint.Style.FILL_AND_STROKE);

        textPaint = new TextPaint();
        textPaint.setColor(Color.WHITE);
        textPaint.setStyle(Paint.Style.FILL_AND_STROKE);
        textPaint.setTextSize(20 * getResources().getDisplayMetrics().density);
    }

//    private void sendText(String text){
//        data = text;
//        this.publishViewData(new SendtextData(data));
//
//        // Redraw
//        invalidate();
//    }
//    @Override
//    public boolean onTouchEvent(MotionEvent event) {
//        if (this.editMode) {
//            return super.onTouchEvent(event);
//        }
//
//        switch (event.getActionMasked()) {
//            case MotionEvent.ACTION_UP:
////                EditText simpleEditText = (EditText) findViewById(R.id.simpleEditText);
//                textPaint.setColor(getResources().getColor(R.color.colorPrimary));
//                sendText(data);
//                break;
//            case MotionEvent.ACTION_DOWN:
//                sendText(data);
//                break;
//            default:
//                return false;
//        }
//
//        return true;
//    }

    @Override
    public void onDraw(Canvas canvas) {
        super.onDraw(canvas);

        float width = getWidth();
        float height = getHeight();
        float textLayoutWidth = width;

        SendtextEntity entity = (SendtextEntity) widgetEntity;

        if (entity.rotation == 90 || entity.rotation == 270) {
            textLayoutWidth = height;
        }

        canvas.drawRect(new Rect(0, 0, (int) width, (int) height), backgroundPaint);

        staticLayout = new StaticLayout(entity.text,
                textPaint,
                (int) textLayoutWidth,
                Layout.Alignment.ALIGN_CENTER,
                1.0f,
                0,
                false);
        canvas.save();
        canvas.rotate(entity.rotation, width / 2, height / 2);
        canvas.translate(((width / 2) - staticLayout.getWidth() / 2), height / 2 - staticLayout.getHeight() / 2);
        staticLayout.draw(canvas);
        canvas.restore();
    }
}
