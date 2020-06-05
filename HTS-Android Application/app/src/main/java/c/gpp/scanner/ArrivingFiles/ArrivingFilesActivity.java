package c.gpp.scanner.ArrivingFiles;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import c.gpp.scanner.R;
import c.gpp.scanner.Scan.ScanCodeActivity;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import android.annotation.TargetApi;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Authenticator;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.PasswordAuthentication;
import java.net.URL;
import java.util.ArrayList;
import java.util.Iterator;

import static c.gpp.scanner.Login.MainActivity.postUrl;
import static java.lang.Long.valueOf;

public class ArrivingFilesActivity extends AppCompatActivity {

    static String postUrl_arrfile = postUrl + "/get_emp_stats";
    static String postUrl_notify = postUrl + "/file_not_arrived_complain";
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    RecyclerView recyclerView;
    LinearLayoutManager linearLayoutManager;
    AFcustomAdapter customAdapter;
    FloatingActionButton scanbtn;
    ProgressDialog progressDialog;
    static String email;


    ArrayList<Aflistpojo> list = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_arriving_files);


        /*****************************************Shared pref************************************************/
        saved = getApplicationContext().getSharedPreferences("shared_pref", Context.MODE_PRIVATE);
        saved_edit = saved.edit();
        /*****************************************Shared pref************************************************/
        email = saved.getString("email", "NULL");

        scanbtn = findViewById(R.id.scanbtn);

        scanbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), ScanCodeActivity.class));
            }
        });


        OkHttpHandler okHttpHandler= new OkHttpHandler();
        okHttpHandler.execute(postUrl_arrfile);

    }

    class OkHttpHandler extends AsyncTask<String, String, String> {

        OkHttpClient client = new OkHttpClient();

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            progressDialog = new ProgressDialog(ArrivingFilesActivity.this);
            progressDialog.setMessage("Fetching Files...");
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

            try {
                String loginResponseString = response;
                Log.d("LOGIN", "Response from the server for files : " + loginResponseString);

                JSONObject result = new JSONObject(loginResponseString);
                JSONObject details = result.getJSONObject("details").getJSONObject("incomingFiles");


                Iterator iterator = details.keys();
                while (iterator.hasNext()) {
                    String key = (String) iterator.next();
                    JSONObject file = details.getJSONObject(key);

                    list.add(new Aflistpojo("File ID: " + key,
                            "Remark:" + file.getString("remark"), "Arrival Time: "
                            + file.getString("time"), ""+key,""+file.getString("from"),""+file.get("time"),""+file.get("alert")));
                }

                if (result.getString("status").equals("1")) {
                  //  Toast.makeText(ArrivingFilesActivity.this, "File Recieved Successfuly", Toast.LENGTH_SHORT).show();
                  //  Toast.makeText(ArrivingFilesActivity.this, list.toString(), Toast.LENGTH_SHORT).show();

                    recyclerView = (RecyclerView) findViewById(R.id.files_listview);
                    linearLayoutManager = new LinearLayoutManager(getApplicationContext());
                    recyclerView.setLayoutManager(linearLayoutManager);
                    customAdapter = new AFcustomAdapter(ArrivingFilesActivity.this, list);
                    recyclerView.setAdapter(customAdapter); // set the Adapter to RecyclerView

                } else if (result.getString("status").equals("0")) {
                    Toast.makeText(ArrivingFilesActivity.this, "Failed to send", Toast.LENGTH_SHORT).show();
                } else if (result.getString("status").equals("2")) {
                    Toast.makeText(ArrivingFilesActivity.this, "Method error", Toast.LENGTH_SHORT).show();
                } else if (result.getString("status").equals("3")) {
                    Toast.makeText(ArrivingFilesActivity.this, "Database error", Toast.LENGTH_SHORT).show();
                }
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(ArrivingFilesActivity.this, "No Files Currently", Toast.LENGTH_SHORT).show();

            }

        }
    }




}






