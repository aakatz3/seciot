package com.aakportfolio.aakatz3.seciotapp;

/**
 * Created by Andrew on 10/6/2016.
 */

class iotnode {
    int index;
    private String friendlyName;
    boolean getState(){
        return true;
    }

    public String toString(){
        if(friendlyName == null){
            return "Node " + Integer.toString(index);
        } else {
            return friendlyName;
        }
    }
}
