package com.aakportfolio.aakatz3.seciotapp;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;


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

    public void pollState() throws Exception{

        String url = SERVER_URL + "poll/";

        JSONObject postParams = new JSONObject();

        postParams.put("guid", guid);
        postParams.put("home_or_mobile", Integer.toString(iotsettings.IOT_MOBILE_DEVICE));
        Log.d("json", postParams.toString());


        Log.d("test", secureAPI.toString());
        Log.d("test", url);
        Log.d("test", postParams.toString());


        SecIOTHelerParams secIOTHelerParams = new SecIOTHelerParams(secureAPI, url, postParams);

        new SecIOTHelper().execute(secIOTHelerParams);
    }
    private class SecIOTHelerParams{
        SecureAPI secureAPI;
        JSONObject jso;
        String url;
        SecIOTHelerParams(SecureAPI secureAPI, String url, JSONObject jso){
            this.secureAPI = secureAPI;
            this.jso = jso;
            this.url = url;
        }
    }

    private class SecIOTHelper extends AsyncTask<SecIOTHelerParams, JSONObject, JSONObject> {



        @Override
        protected JSONObject doInBackground(SecIOTHelerParams... params) {
            try{
                HashMap<String, String> map = new HashMap<>();
                map.put("a","b");
                //return params[0].secureAPI.HTTPSPOSTJSON(params[0].url, map);
                return params[0].secureAPI.HTTPSPOSTJSON(params[0].url,params[0].jso);
            }catch(Exception e){
                e.printStackTrace();
                return null;
            }
        }

        @Override
        protected void onPostExecute(JSONObject v) {
            if(v != null) {
                Log.d("json", v.toString());
            } else {
                Log.d("json", "NULL");
            }
        }
    }


}
