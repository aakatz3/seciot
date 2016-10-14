package com.aakportfolio.aakatz3.seciotapp;

/**
 * Created by Andrew on 10/6/2016.
 */

class iotnode {
    int index;
    String friendlyName;
    boolean state;

    public iotnode(int index, String friendlyName, boolean state){
        this.state = state;
        this.index = index;
        this.friendlyName = friendlyName;
    }

    boolean getState(){
        return state;
    }
    void setState(boolean state){
        this.state = state;
    }

    public String toString(){
        if(friendlyName == null){
            return "Node " + Integer.toString(index);
        } else {
            return friendlyName;
        }
    }
}
