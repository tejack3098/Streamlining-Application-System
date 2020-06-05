package c.gpp.scanner.CurrentFiles;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import c.gpp.scanner.ArrivingFiles.AFcustomAdapter;
import c.gpp.scanner.ArrivingFiles.Aflistpojo;
import c.gpp.scanner.ArrivingFiles.ArrivingFilesActivity;
import c.gpp.scanner.R;
import okhttp3.Call;
import okhttp3.Callback;
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

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;

import static c.gpp.scanner.Login.MainActivity.postUrl;

public class CurFilesActivity extends AppCompatActivity {

    static String postUrl3 = postUrl+ "/get_emp_stats";
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    RecyclerView recyclerView;
    LinearLayoutManager linearLayoutManager;
    CustomAdapter customAdapter;
    ProgressDialog progressDialog;

    ArrayList<ListPojo> list = new ArrayList<ListPojo>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cur_files);

        /*****************************************Shared pref************************************************/
        saved = getApplicationContext().getSharedPreferences("shared_pref", Context.MODE_PRIVATE);
        saved_edit = saved.edit();
        /*****************************************Shared pref************************************************/

        OkHttpHandler okHttpHandler= new OkHttpHandler();
        okHttpHandler.execute(postUrl3);



    }


    class OkHttpHandler extends AsyncTask<String, String, String> {

        OkHttpClient client = new OkHttpClient();

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            progressDialog = new ProgressDialog(CurFilesActivity.this);
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

                JSONObject result= new JSONObject(loginResponseString);
                JSONObject details=  result.getJSONObject("details");

                JSONArray jsonArray = details.getJSONArray("currFiles");
                if(jsonArray.length()==0){
                    Toast.makeText(CurFilesActivity.this, "No Current Files yet.", Toast.LENGTH_SHORT).show();
                }

                Log.d("resp", "json array : " + jsonArray);
                for(int i = 0 ; i < jsonArray.length(); i++) {
                    list.add(new ListPojo(jsonArray.getJSONObject(i).getString("fid"),
                            "Delay :" + jsonArray.getJSONObject(i).getString("delay"), "Arrival Time:"
                            + jsonArray.getJSONObject(i).getString("timeArrived")));
                }

                if (result.getString("status").equals("1")) {
                   // Toast.makeText(CurFilesActivity.this, "File Recieved Successfuly", Toast.LENGTH_SHORT).show();
                   // Toast.makeText(CurFilesActivity.this, list.toString(), Toast.LENGTH_SHORT).show();

                    recyclerView = (RecyclerView) findViewById(R.id.files_listview);
                    // set a LinearLayoutManager with default vertical orientation
                    linearLayoutManager = new LinearLayoutManager(getApplicationContext());
                    recyclerView.setLayoutManager(linearLayoutManager);
                    // call the constructor of CustomAdapter to send the reference and data to Adapter
                    customAdapter = new CustomAdapter(CurFilesActivity.this, list);
                    recyclerView.setAdapter(customAdapter); // set the Adapter to RecyclerView

                } else if (result.getString("status").equals("0")) {
                    Toast.makeText(CurFilesActivity.this, "Failed to send", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Failed to send");
                }else if(result.getString("status").equals("2")){
                    Toast.makeText(CurFilesActivity.this, "Method error", Toast.LENGTH_SHORT).show();
                    //responseTextLogin.setText("Method error");
                }else if(result.getString("status").equals("3")){
                    Toast.makeText(CurFilesActivity.this, "Database error", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Database error");
                }
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(CurFilesActivity.this, "Something went wrong. Please try again later.", Toast.LENGTH_SHORT).show();

            }



        }
    }



}
