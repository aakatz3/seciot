package com.aakportfolio.aakatz3.seciotapp;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;


/**
 * Created by Andrew on 9/16/2016.
 */
public class seciot {
    private static final String SERVER_URL = "https://osrsrv.aakportfolio.com/";
    private String guid;
    private ArrayList<iotnode> nodes;
    private SecureAPI secureAPI;

    SecIOTPollCompleteListener secIOTPollCompleteListener;

    public void updateGuid(String guid){
        this.guid = guid;
    }

    public seciot(String guid, SecureAPI secureAPI, SecIOTPollCompleteListener listener){
        this.guid = guid;
        nodes = new ArrayList<>(10);
        for(int i = 0; i < 10; i++){
            nodes.add(new iotnode((i + 1), null, false));
        }
       this.secureAPI = secureAPI;
        secIOTPollCompleteListener = listener;
    }

    public seciot(SecureAPI secureAPI, SecIOTPollCompleteListener listener){
        this.guid = null;
        nodes = new ArrayList<>(10);
        for(int i = 0; i < 10; i++){
            nodes.add(new iotnode((i + 1), null, false));
        }
        this.secureAPI = secureAPI;
        secIOTPollCompleteListener = listener;
    }

    public ArrayList<iotnode> getNodes(){
        return nodes;
    }
    public void setNodes(ArrayList<iotnode> nodes){
        this.nodes = nodes;
        if(secIOTPollCompleteListener != null){
            secIOTPollCompleteListener.performUpdate();
        }
    }
    public void setState(int node, boolean state){
        nodes.get(node).setState(state);
    }
    public void pushState() throws JSONException {
        //YYYY-MM-DD HH:MM:SS (24)
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String formattedDate = df.format(Calendar.getInstance().getTime());
        ArrayList<JSONArray> switches = new ArrayList<>();
        for(iotnode n : nodes) {
          /*  ArrayList<Object> switchObj = new ArrayList<>();
            switchObj.add(n.friendlyName);
            if(n.state){
                switchObj.add("1");
            } else {
                switchObj.add("0");
            }
            switchObj.add(formattedDate);
            switchObj.add(0);
            switches.add(new JSONArray(switchObj));*/
            //switches.add(new JSONArray("[\"" + n.friendlyName + "\"," + (n.state ? "\"1\",\"" : "\"0\",\"") +  formattedDate + "\",0]"));
            switches.add(new JSONArray("['" + n.friendlyName + "'," + (n.state ? "'1','" : "'0','") +  formattedDate + "',0]"));
        }

        JSONArray arr = new JSONArray(switches);

        String url = SERVER_URL + "push/";

        JSONObject postParams = new JSONObject();

        postParams.put("guid", guid);
        postParams.put("home_or_mobile", Integer.toString(iotsettings.IOT_MOBILE_DEVICE));
        postParams.put("state", arr.toString());

        String jsstr = postParams.toString();

        jsstr = jsstr.replace("\\\"", "\"");
        jsstr = jsstr.replace("\"[", "[");
        jsstr = jsstr.replace("]\"", "]");

        postParams = new JSONObject(jsstr);

        Log.d("json", postParams.toString());

        SecIOTHelerParams secIOTHelerParams = new SecIOTHelerParams(secureAPI, url, postParams, null);

        new SecIOTHelper().execute(secIOTHelerParams);
        //return null;
    }



    public void pollState(SecIOTPollCompleteListener listener) throws Exception{
        pollState(listener, iotsettings.IOT_HOME_NODE);
    }

    public void pollState(SecIOTPollCompleteListener listener, int homeOrMobile) throws Exception{
        String url = SERVER_URL + "poll/";

        JSONObject postParams = new JSONObject();

        postParams.put("guid", guid);
        postParams.put("home_or_mobile", Integer.toString(homeOrMobile));
        Log.d("json", postParams.toString());

        SecIOTHelerParams secIOTHelerParams = new SecIOTHelerParams(secureAPI, url, postParams, listener);

        new SecIOTHelper().execute(secIOTHelerParams);
    }
    private class SecIOTHelerParams{
        SecureAPI secureAPI;
        JSONObject jso;
        String url;
        SecIOTPollCompleteListener listener;

        SecIOTHelerParams(SecureAPI secureAPI, String url, JSONObject jso, SecIOTPollCompleteListener listener){
            this.secureAPI = secureAPI;
            this.jso = jso;
            this.url = url;
            this.listener = listener;
        }
    }

    private class SecIOTHelper extends AsyncTask<SecIOTHelerParams, JSONObject, JSONObject> {
        SecIOTHelerParams myParams;


        @Override
        protected JSONObject doInBackground(SecIOTHelerParams... params) {
            myParams = params[0];
            try{
                HashMap<String, String> map = new HashMap<>();
                map.put("a","b");
                //return params[0].secureAPI.HTTPSPOSTJSON(params[0].url, map);
                return myParams.secureAPI.HTTPSPOSTJSON(myParams.url,myParams.jso);
            }catch(Exception e){
                e.printStackTrace();
                return null;
            }
        }

        @Override
        protected void onPostExecute(JSONObject v) {
            if(v != null) {
                Log.d("json", v.toString());
                updateState(v);
            } else {
                Log.d("json", "NULL");
            }
        }
    }

    public void updateState(JSONObject recievedStates){
        JSONArray array = null;
        try {
            array = recievedStates.getJSONArray("state");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        if(array != null){
            ArrayList<iotnode> nodes = new ArrayList<>();
            for (int i = 0; i < array.length(); i++){
                try {
                    Log.d("JSO-sw", array.get(i).toString());
                    JSONArray node = ((JSONArray) array.get(i));
                    Log.d("JSO-sw", node.get(1).toString());
                    nodes.add(new iotnode(i + 1, node.get(0).toString(), (node.get(1).toString().equals("1"))));
                } catch (JSONException e) {
                    e.printStackTrace();
                    Log.d("JSO-sw", "err");
                }
            }
            if(nodes.size() > 0){
                setNodes(nodes);
            }
        }
    }

    interface SecIOTPollCompleteListener{
        public void performUpdate();
    }

}
