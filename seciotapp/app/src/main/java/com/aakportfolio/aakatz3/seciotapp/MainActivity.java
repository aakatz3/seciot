package com.aakportfolio.aakatz3.seciotapp;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.SharedPreferences;
import android.provider.Settings;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.preference.PreferenceManager;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Array;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity implements View.OnClickListener, seciot.SecIOTPollCompleteListener{

    LinearLayout controlLayout;
    EditText guid_text;
    Button guid_submit;
    SharedPreferences prefs;
    String guid;

    SecureAPI secureAPI;

    seciot foobar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        prefs = getPreferences(Context.MODE_PRIVATE);
        secureAPI = SecureAPI.getInstance(this);

        guid = prefs.getString("guid", null);

        foobar = new seciot(guid, secureAPI, this);


        controlLayout = (LinearLayout) findViewById(R.id.control_layout);
        guid_submit = (Button)findViewById(R.id.guid_submit);
        guid_submit.setOnClickListener(this);
        guid_text = (EditText) findViewById(R.id.editText);
        guid_text.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
                if(actionId == EditorInfo.IME_ACTION_DONE){
                    guid_submit.performClick();
                    return true;
                }
                return false;
            }
        });

        if(guid != null){
            guid_text.setText(guid);
            try {
                foobar.pollState(this);
            } catch (Exception ex){
                ex.printStackTrace();
            }
        }
    }



    public void performUpdate(){
        controlLayout.removeAllViews();


        for(iotnode n : foobar.getNodes()){
            CheckBox cb = new CheckBox(this);
            n.index = foobar.getNodes().indexOf(n);
            cb.setText(n.toString());
            cb.setChecked(n.getState());
            final int idx = n.index;
            cb.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    //foobar.setState(idx, isChecked);
                    Log.d("box", ""+idx);
                    try {
                        foobar.setState(idx, isChecked);
                        foobar.pushState();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    Toast.makeText(getApplicationContext(), buttonView.getText(), Toast.LENGTH_SHORT).show();
                }
            });
            controlLayout.addView(cb);
        }
    }

    @SuppressLint("CommitPrefEdits")
    @Override
    public void onClick(View v) {
        switch(v.getId()){
            case R.id.guid_submit:
                guid = guid_text.getText().toString();
                prefs.edit().putString("guid",guid).commit();
                foobar.updateGuid(guid);
                try {
                    foobar.pollState(this);
                } catch (Exception ex){
                    ex.printStackTrace();
                }
                break;
            default:
                Toast.makeText(this, "Not Implemented", Toast.LENGTH_SHORT).show();
        }
    }
}
