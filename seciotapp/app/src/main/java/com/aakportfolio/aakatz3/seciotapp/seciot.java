package com.aakportfolio.aakatz3.seciotapp;

import android.content.Context;
import android.util.Log;

import org.json.JSONObject;

import java.util.ArrayList;


/**
 * Created by Andrew on 9/16/2016.
 */
public class seciot {
    private static final String SERVER_URL = "https://osrsrv.aakportfolio.com/";
    private String guid;
    private ArrayList<iotnode> nodes;
    private SecureAPI secureAPI;
    public seciot(String guid, SecureAPI secureAPI){
        this.guid = guid;
        nodes = new ArrayList<>(10);
        for(int i = 0; i < 10; i++){
            nodes.add(new iotnode());
        }
       this.secureAPI = secureAPI;
    }

    public ArrayList<iotnode> getNodes(){
        return nodes;
    }
    public JSONObject pushState(int idx, boolean state)
    {
        return null;
    }

    public JSONObject pollState() throws Exception{

        String url = SERVER_URL + "poll/";

        JSONObject postParams = new JSONObject();

        postParams.put("guid", guid);
        postParams.put("home_or_mobile", Integer.toString(iotsettings.IOT_MOBILE_DEVICE));
        Log.d("json", postParams.toString());

        secureAPI.HTTPSGETJSON(url);

        JSONObject jso = secureAPI.HTTPSPOSTJSON(url, postParams);

        //USE A MF. ASYNC TASK!!!!!!!

        return jso;
    }
}
