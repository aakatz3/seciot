package com.aakportfolio.aakatz3.seciotapp;

import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.preference.PreferenceManager;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    LinearLayout controlLayout;
    EditText guid;
    SharedPreferences prefs;

    seciot foobar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        prefs = PreferenceManager.getDefaultSharedPreferences(this);

        controlLayout = (LinearLayout) findViewById(R.id.control_layout);

        SecureAPI secureAPI = SecureAPI.getInstance(this);

        foobar = new seciot(prefs.getString("guid", "sfasdasdfa"), secureAPI);
        int count = 0;
        for(iotnode n : foobar.getNodes()){
            CheckBox cb = new CheckBox(this);
            n.index = foobar.getNodes().indexOf(n);
            cb.setText(n.toString());
            cb.setChecked(n.getState());
            //final int idx = n.index;
            cb.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    //foobar.setState(idx, isChecked);
                    Toast.makeText(getApplicationContext(), buttonView.getText(), Toast.LENGTH_SHORT).show();
                }
            });
            count++;
            try {
                foobar.pollState();
            } catch (Exception ex){
                ex.printStackTrace();
            }
            controlLayout.addView(cb);
        }
    }
}
