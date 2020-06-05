package c.gpp.scanner.EmpStats;

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
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import static c.gpp.scanner.Login.MainActivity.postUrl;

public class EmpStatsActivity extends AppCompatActivity {

    TextView email,dname,deptid,mno,totalfiles,comontime,delayedfiles;
    ProgressBar effbar;

    static String postUrl_profile= postUrl+ "/get_emp_data_for_rating";
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    ProgressDialog progressDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_emp_stats);

        email = findViewById(R.id.email);
        dname =  findViewById(R.id.deptname);
        deptid = findViewById(R.id.deptid);
        mno = findViewById(R.id.mno);
        totalfiles = findViewById(R.id.totalfiles);
        comontime = findViewById(R.id.comontime);
        delayedfiles = findViewById(R.id.delayedfiles);
        effbar = findViewById(R.id.effbar);

        /*****************************************Shared pref************************************************/
        saved = getApplicationContext().getSharedPreferences("shared_pref", Context.MODE_PRIVATE);
        saved_edit = saved.edit();
        /*****************************************Shared pref************************************************/

       OkHttpHandler okHttpHandler= new OkHttpHandler();
        okHttpHandler.execute(postUrl_profile);


    }


    class OkHttpHandler extends AsyncTask<String, String, String> {

        OkHttpClient client = new OkHttpClient();

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            progressDialog = new ProgressDialog(EmpStatsActivity.this);
            progressDialog.setMessage("Fetching Details...");
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

      /*      Toast.makeText(EmpStatsActivity.this, response, Toast.LENGTH_SHORT).show();*/


            try {


                JSONObject result = new JSONObject(response);
                JSONObject t = result.getJSONObject("details");


                if (result.getString("status").equals("1")) {
                    //Toast.makeText(PreviousFilesActivity.this, "File Recieved Successfuly", Toast.LENGTH_SHORT).show();
                    //Toast.makeText(PreviousFilesActivity.this, list.toString(), Toast.LENGTH_SHORT).show();

                    email.setText("Email ID: " +t.getString("email_id"));
                    dname.setText("Department Name: "+ t.getString("dept_name"));
                    deptid.setText("Department ID: "+ t.getString("dept_id"));
                    mno.setText("Mobile No.: "+ t.getString("mno"));

                    int totalcnt = Integer.parseInt(t.getString("prevFilesCount"));
                    totalfiles.setText("Total Files: "+Integer.toString(totalcnt));
                    int delaycnt = Integer.parseInt(t.getString("prevFilesWithDelay"));


                    int ontimecnt = totalcnt - delaycnt;
                    double e = (double)ontimecnt/totalcnt;
                    comontime.setText("Completed On Time: "+Integer.toString(ontimecnt));
                    delayedfiles.setText("Delayed: "+Integer.toString(delaycnt));
                    int m = (int)(e * 100);
                    effbar.setProgress(m);



                } else if (result.getString("status").equals("0")) {
                    Toast.makeText(EmpStatsActivity.this, "Failed to send", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Failed to send");
                }else if(result.getString("status").equals("2")){
                    Toast.makeText(EmpStatsActivity.this, "Method error", Toast.LENGTH_SHORT).show();
                    //responseTextLogin.setText("Method error");
                }else if(result.getString("status").equals("3")){
                    Toast.makeText(EmpStatsActivity.this, "Database error", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Database error");
                }
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(EmpStatsActivity.this, "Something went wrong. Please try again later.", Toast.LENGTH_SHORT).show();

            }





        }
    }

    class Markallread extends AsyncTask<String, String, String> {

        OkHttpClient client = new OkHttpClient();

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            progressDialog = new ProgressDialog(EmpStatsActivity.this);
            progressDialog.setMessage("Fetching Details...");
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

            /*      Toast.makeText(EmpStatsActivity.this, response, Toast.LENGTH_SHORT).show();*/


            try {


                JSONObject result = new JSONObject(response);
                JSONObject t = result.getJSONObject("details");


                if (result.getString("status").equals("1")) {
                    //Toast.makeText(PreviousFilesActivity.this, "File Recieved Successfuly", Toast.LENGTH_SHORT).show();
                    //Toast.makeText(PreviousFilesActivity.this, list.toString(), Toast.LENGTH_SHORT).show();

                    email.setText("Email ID: " +t.getString("email_id"));
                    dname.setText("Department Name: "+ t.getString("dept_name"));
                    deptid.setText("Department ID: "+ t.getString("dept_id"));
                    mno.setText("Mobile No.: "+ t.getString("mno"));

                    int totalcnt = Integer.parseInt(t.getString("prevFilesCount"));
                    totalfiles.setText("Total Files: "+Integer.toString(totalcnt));
                    int delaycnt = Integer.parseInt(t.getString("prevFilesWithDelay"));


                    int ontimecnt = totalcnt - delaycnt;
                    double e = (double)ontimecnt/totalcnt;
                    comontime.setText("Completed On Time: "+Integer.toString(ontimecnt));
                    delayedfiles.setText("Delayed: "+Integer.toString(delaycnt));
                    int m = (int)(e * 100);
                    effbar.setProgress(m);



                } else if (result.getString("status").equals("0")) {
                    Toast.makeText(EmpStatsActivity.this, "Failed to send", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Failed to send");
                }else if(result.getString("status").equals("2")){
                    Toast.makeText(EmpStatsActivity.this, "Method error", Toast.LENGTH_SHORT).show();
                    //responseTextLogin.setText("Method error");
                }else if(result.getString("status").equals("3")){
                    Toast.makeText(EmpStatsActivity.this, "Database error", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Database error");
                }
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(EmpStatsActivity.this, "Something went wrong. Please try again later.", Toast.LENGTH_SHORT).show();

            }





        }
    }

}
