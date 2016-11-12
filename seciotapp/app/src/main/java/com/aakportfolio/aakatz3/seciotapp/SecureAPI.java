package com.aakportfolio.aakatz3.seciotapp;


import android.content.Context;
import android.util.Log;

import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.net.URLEncoder;
import java.security.KeyStore;
import java.security.cert.Certificate;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.Map;
import java.util.Scanner;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManagerFactory;

/**
 * Handles secure server communications
 * SecureAPI singleton class
 * Created by Andrew Katz
 */
public class SecureAPI {

    private static SecureAPI mySecureAPI = null;
    private SSLSocketFactory mySocketFactory = null;



    public static SecureAPI getInstance(Context c){
        if( mySecureAPI == null){
            try {
                mySecureAPI = new SecureAPI(c.getApplicationContext()
                        .getResources().openRawResource(R.raw.cabundle));
            }catch (Exception e){
                Log.d("SecureAPI Exception",e.getMessage());
            }
        }
        return mySecureAPI;
    }
    public static SecureAPI getInstance() throws Exception {
        if( mySecureAPI == null){
            throw new NullPointerException();
        }
        return getInstance(null);
    }
    private void createSocketFactory(InputStream is) throws Exception {
        CertificateFactory certificateFactory = CertificateFactory.getInstance("X.509");
        Certificate certificate = certificateFactory.generateCertificate(is);
        Log.d("SecureAPI", "ca=" + ((X509Certificate) certificate).getSubjectDN());


        KeyStore keyStore = KeyStore.getInstance(KeyStore.getDefaultType());
        keyStore.load(null, null);
        keyStore.setCertificateEntry("ca", certificate);

        TrustManagerFactory trustManagerFactory =
                TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        trustManagerFactory.init(keyStore);

        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(null, trustManagerFactory.getTrustManagers(), null);

        mySocketFactory = sslContext.getSocketFactory();
    }

    private String getPostString(Map<String, String> params) throws Exception {
        StringBuilder stringBuilder = new StringBuilder();
        boolean first = true;
        for(Map.Entry<String, String> p : params.entrySet()) {
            if(first)
                first = false;
            else
                stringBuilder.append("&");

            stringBuilder.append(URLEncoder.encode(p.getKey(), "UTF-8"));
            stringBuilder.append("=");
            stringBuilder.append(URLEncoder.encode(p.getValue(), "UTF-8"));
        }
        return stringBuilder.toString();
    }

    private String getResponseFromStream(InputStream is) {
        Scanner scanner = new java.util.Scanner(is).useDelimiter("\\A");
        return scanner.hasNext() ? scanner.next() : "";
    }

    private SecureAPI(InputStream inputStream) throws Exception {
        this.createSocketFactory(inputStream);
    }



    public JSONObject HTTPSPOSTJSON(String urlString, JSONObject json) throws Exception {
        URL url = new URL(urlString);
        HttpsURLConnection httpsURLConnection = (HttpsURLConnection) url.openConnection();
/*
        httpsURLConnection.setSSLSocketFactory(mySocketFactory);
        httpsURLConnection.setReadTimeout(10000);
        httpsURLConnection.setConnectTimeout(15000);
        httpsURLConnection.setUseCaches(false);
        httpsURLConnection.setRequestMethod("POST");
        httpsURLConnection.setRequestProperty("Accept", "application/json");
        httpsURLConnection.setRequestProperty("Content-Type", "application/json");
       // httpsURLConnection.setRequestProperty("Host", "osrsrv.aakportfolio.com");
        httpsURLConnection.setDoInput(true);
        httpsURLConnection.setDoOutput(true);
*/
        httpsURLConnection.setSSLSocketFactory(mySocketFactory);
        httpsURLConnection.setReadTimeout(10000);
        httpsURLConnection.setConnectTimeout(15000);
        httpsURLConnection.setRequestMethod("POST");
        httpsURLConnection.setRequestProperty("Content-Type", "application/json");
        httpsURLConnection.setDoInput(true);
        httpsURLConnection.setDoOutput(true);

        //String request = URLEncoder.encode(json.toString(), "UTF-8");
        String request = json.toString();

        Log.d("request", request);


       httpsURLConnection.connect();

        DataOutputStream outputStream = new DataOutputStream(httpsURLConnection.getOutputStream());
       // outputStream.write(json.toString().getBytes("UTF-8"));

        //OutputStreamWriter wr= new OutputStreamWriter(httpsURLConnection.getOutputStream());
        outputStream.writeBytes(request);
        //wr.write(json.toString());
        //wr.flush();
        //wr.close();
        outputStream.flush();
       /* outputStream.
        BufferedWriter bufferedWriter =
                new BufferedWriter(new OutputStreamWriter(outputStream, "UTF-8"));
        bufferedWriter.write(json.toString());*/
        //bufferedWriter.flush();
        //bufferedWriter.close();
        outputStream.close();

        httpsURLConnection.connect();

        String response = "";

        try{
            response = getResponseFromStream(httpsURLConnection.getInputStream());
            response = response.replace("\\\"", "\"");
            response = response.replace("\"[", "[");
            response = response.replace("]\"", "]");
        } catch(FileNotFoundException e){
            e.printStackTrace();
            response = getResponseFromStream(httpsURLConnection.getErrorStream());
            Log.d("httpserror", response);
        }

        return new JSONObject(response);
    }

}
