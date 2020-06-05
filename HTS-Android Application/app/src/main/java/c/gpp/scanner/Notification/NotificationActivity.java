package c.gpp.scanner.Notification;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import c.gpp.scanner.PreviousFiles.Pf_listpojo;
import c.gpp.scanner.PreviousFiles.PfcustomAdapter;
import c.gpp.scanner.PreviousFiles.PreviousFilesActivity;
import c.gpp.scanner.R;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

import static c.gpp.scanner.Login.MainActivity.postUrl;

public class NotificationActivity extends AppCompatActivity {

    static String postUrl_notify= postUrl+ "/get_emp_notifications";
    static String postUrl_markallread= postUrl+ "/update_all_notifications_status";

    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    RecyclerView recyclerView;
    LinearLayoutManager linearLayoutManager;
    NcustomAdapter customAdapter;
    ProgressDialog progressDialog;

    ArrayList<NListPojo> list = new ArrayList<NListPojo>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notification);

        /*****************************************Shared pref************************************************/
        saved = getApplicationContext().getSharedPreferences("shared_pref", Context.MODE_PRIVATE);
        saved_edit = saved.edit();
        /*****************************************Shared pref************************************************/

        OkHttpHandler okHttpHandler= new OkHttpHandler();
        okHttpHandler.execute(postUrl_notify);




    }

    class OkHttpHandler extends AsyncTask<String, String, String> {

        OkHttpClient client = new OkHttpClient();

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            progressDialog = new ProgressDialog(NotificationActivity.this);
            progressDialog.setMessage("Fetching Notifications...");
            progressDialog.setCancelable(false);
            progressDialog.show();
        }

        @Override
        protected String doInBackground(String... params) {

            JSONObject barcodeTxt = new JSONObject();
            try {

                barcodeTxt.put("email_id", saved.getString("email", "NULL"));

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

            Markallread mar= new Markallread();
            mar.execute(postUrl_markallread);


            try {
                Log.d("LOGIN", "Response from the server for files : " + response);


                JSONObject result= new JSONObject(response);
                JSONArray jsonArray = result.getJSONArray("notifis");
                Log.d("resp", "json array : " + jsonArray);

                if(jsonArray.length()==0){
                    Toast.makeText(NotificationActivity.this, "No New Notifications.", Toast.LENGTH_SHORT).show();
                }

                if (result.getString("status").equals("1")) {

                    if(result.getString("new_notification").equals("1")) {


                        Toast.makeText(NotificationActivity.this, "New Notifications", Toast.LENGTH_SHORT).show();
                        for (int i = 0; i < jsonArray.length(); i++) {



                            if(jsonArray.getJSONObject(i).getString("read").equals("false")) {

                                list.add(new NListPojo("Notification ID:" + jsonArray.getJSONObject(i).getString("notificationID"),
                                        "Message :" + jsonArray.getJSONObject(i).getString("message"), "Time Created:"
                                        + jsonArray.getJSONObject(i).getString("timeCreated"), "new"));

                            }else{

                                list.add(new NListPojo("Notification ID:" + jsonArray.getJSONObject(i).getString("notificationID"),
                                        "Message :" + jsonArray.getJSONObject(i).getString("message"), "Time Created:"
                                        + jsonArray.getJSONObject(i).getString("timeCreated"), "old"));

                            }
                        }

                    }else{

                        Toast.makeText(NotificationActivity.this, "Old Notifications", Toast.LENGTH_SHORT).show();
                        for (int i = 0; i < jsonArray.length(); i++) {
                            list.add(new NListPojo("Notification ID:" + jsonArray.getJSONObject(i).getString("notificationID"),
                                    "Message :" + jsonArray.getJSONObject(i).getString("message"), "Time Created:"
                                    + jsonArray.getJSONObject(i).getString("timeCreated"),"old"));
                        }

                    }


                    recyclerView = (RecyclerView) findViewById(R.id.notify_listview);
                    // set a LinearLayoutManager with default vertical orientation
                    linearLayoutManager = new LinearLayoutManager(getApplicationContext());
                    recyclerView.setLayoutManager(linearLayoutManager);
                    // call the constructor of CustomAdapter to send the reference and data to Adapter
                    customAdapter = new NcustomAdapter(NotificationActivity.this, list);
                    recyclerView.setAdapter(customAdapter); // set the Adapter to RecyclerView

                } else if (result.getString("status").equals("0")) {
                    Toast.makeText(NotificationActivity.this, "Failed to send", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Failed to send");
                }else if(result.getString("status").equals("2")){
                    Toast.makeText(NotificationActivity.this, "Method error", Toast.LENGTH_SHORT).show();
                    //responseTextLogin.setText("Method error");
                }else if(result.getString("status").equals("3")){
                    Toast.makeText(NotificationActivity.this, "Database error", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Database error");
                }
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(NotificationActivity.this, "Something went wrong. Please try again later.", Toast.LENGTH_SHORT).show();

            }





        }
    }

    class Markallread extends AsyncTask<String, String, String> {

        OkHttpClient client = new OkHttpClient();


        @Override
        protected String doInBackground(String... params) {

            JSONObject barcodeTxt = new JSONObject();
            try {

                barcodeTxt.put("email_id", saved.getString("email", "NULL"));

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


           // Toast.makeText(NotificationActivity.this, response, Toast.LENGTH_SHORT).show();
            try {
                Log.d("LOGIN", "Response from the server for mark all read : " + response);

                JSONObject result= new JSONObject(response);


                if (result.getString("status").equals("1")) {

                  //  Toast.makeText(NotificationActivity.this, "All Marked Read", Toast.LENGTH_SHORT).show();

                } else if (result.getString("status").equals("0")) {
                    Toast.makeText(NotificationActivity.this, "Failed to send", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Failed to send");
                }else if(result.getString("status").equals("2")){
                    Toast.makeText(NotificationActivity.this, "Method error", Toast.LENGTH_SHORT).show();
                    //responseTextLogin.setText("Method error");
                }else if(result.getString("status").equals("3")){
                    Toast.makeText(NotificationActivity.this, "Database error", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Database error");
                }
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(NotificationActivity.this, "Something went wrong. Please try again later.", Toast.LENGTH_SHORT).show();

            }





        }
    }
}
