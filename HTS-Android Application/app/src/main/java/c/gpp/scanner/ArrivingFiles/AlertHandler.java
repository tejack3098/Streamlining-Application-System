package c.gpp.scanner.ArrivingFiles;


import android.app.ProgressDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.sql.Timestamp;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class AlertHandler extends AsyncTask<String, String, String> {

    OkHttpClient client = new OkHttpClient();
    private Context context;
    ProgressDialog progressDialog;
    String fileID,from,time;
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    String notifyId;


    public AlertHandler(Context context,String fileID,String from,String time){
        this.context=context;
        this.fileID=fileID;
        this.from = from;
        this.time = time;
    }



    @Override
    protected void onPreExecute() {
        super.onPreExecute();
        progressDialog = new ProgressDialog(context);
        progressDialog.setMessage("Sending alert...");
        progressDialog.setCancelable(false);
        progressDialog.show();
    }

    @Override
    protected String doInBackground(String... params) {

        JSONObject barcodeTxt = new JSONObject();
        try {

            notifyId = fileID + ArrivingFilesActivity.email;
      /*      DateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS");
            Date date = formatter.parse(time);
            Timestamp ts=new Timestamp(date.getTime());*/
            barcodeTxt.put("notificationid",notifyId);
            barcodeTxt.put("email", ArrivingFilesActivity.email);
            barcodeTxt.put("file",fileID);
            barcodeTxt.put("from",from);
            barcodeTxt.put("time",time);
            barcodeTxt.put("app","app");

        } catch (JSONException e) {
            e.printStackTrace();
        }

        RequestBody body = RequestBody.create(MediaType.parse("application/json; charset=utf-8"), barcodeTxt.toString());

        Request.Builder builder = new Request.Builder();
        builder.url(params[0]);
        builder.post(body);
        builder.header("Accept", "application/json");
        builder.header("Content-Type", "application/json");
        Request request = builder.build();

        try {
            Response response = client.newCall(request).execute();
            return response.body().string();
        }catch (Exception e){
            e.printStackTrace();
        }

        return null;
    }

    @Override
    protected void onPostExecute(String response) {
        super.onPostExecute(response);
        progressDialog.dismiss();

        try {



            Toast.makeText(context, response, Toast.LENGTH_SHORT).show();
            JSONObject result= new JSONObject(response);
          /*  JSONObject result = new JSONObject(loginResponseString);*/

            if (result.getString("status").equals("1")) {
                Toast.makeText(context, "Alert Send Successfully", Toast.LENGTH_SHORT).show();

            } else if (result.getString("status").equals("0")) {
                Toast.makeText(context, "Failed to send", Toast.LENGTH_SHORT).show();
            } else if (result.getString("status").equals("2")) {
                Toast.makeText(context, "Method error", Toast.LENGTH_SHORT).show();
            } else if (result.getString("status").equals("3")) {
                Toast.makeText(context,"Database error", Toast.LENGTH_SHORT).show();
            }
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(context,"No Files Currently", Toast.LENGTH_SHORT).show();

        }

    }
}