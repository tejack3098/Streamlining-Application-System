package c.gpp.scanner.CurrentFiles;


import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;

import androidx.fragment.app.DialogFragment;
import androidx.fragment.app.Fragment;
import c.gpp.scanner.ArrivingFiles.Aflistpojo;
import c.gpp.scanner.R;
import okhttp3.HttpUrl;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.AdapterView;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Spinner;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import static c.gpp.scanner.Login.MainActivity.const_posturl;
import static c.gpp.scanner.Login.MainActivity.postUrl;


/**
 * A simple {@link Fragment} subclass.
 */
public class MyRemarkFragment extends DialogFragment {

    Spinner email_spin;
    ArrayList<Dept_emails> mDept_emails;
    Email_Spinner_Adapter email_spinner_adapter;
    private RadioGroup radioGroup;

    String selectedforward;
    String selectedNextEmail;

    static String postUrl_forward = postUrl+ "/forward";
    static String postUrl_get_dept_employees = postUrl+ "/get_dept_employees";
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    EditText remark;
    String fname;
    private Activity mActivity;
    ProgressDialog progressDialog;

    String dept_id;

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
        mActivity = activity;
    }

    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {

        /*****************************************Shared pref************************************************/
        saved = getContext().getSharedPreferences("shared_pref", Context.MODE_PRIVATE);
        saved_edit = saved.edit();
        /*****************************************Shared pref************************************************/

        dept_id = saved.getString("dept_id", "NULL");

        Bundle bundle = getArguments();
        fname = bundle.getString("fname","");



        AlertDialog.Builder bd = new AlertDialog.Builder(getActivity());
        LayoutInflater inflater = getActivity().getLayoutInflater();

        View DialogView = inflater.inflate(R.layout.fragment_my_remark,null);

       remark = DialogView.findViewById(R.id.remark);
       email_spin = DialogView.findViewById(R.id.emp_email_spinner);
        mDept_emails = new ArrayList<>();

        Get_dept_emails dept_email_handler= new Get_dept_emails();
        dept_email_handler.execute(postUrl_get_dept_employees);

        radioGroup = (RadioGroup)DialogView.findViewById(R.id.forward_radio);
        // Uncheck or reset the radio buttons initially
        radioGroup.clearCheck();

        // Add the Listener to the RadioGroup
        radioGroup.setOnCheckedChangeListener(
                new RadioGroup
                        .OnCheckedChangeListener() {
                    @Override
                    public void onCheckedChanged(RadioGroup group,int checkedId)
                    {

                        // Get the selected Radio Button
                        RadioButton radioButton= (RadioButton)group.findViewById(checkedId);
                        selectedforward = (String) radioButton.getText();

                        if(selectedforward.equals("Forward To next Department")){
                            email_spin.setVisibility(View.GONE);
                        }else{
                            email_spin.setVisibility(View.VISIBLE);
                        }
                      //  Toast.makeText(mActivity, selectedforward, Toast.LENGTH_SHORT).show();
                    }
                });

        bd.setView(DialogView).setTitle("Add Remark").setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                Toast.makeText(getActivity(), "canceled operation", Toast.LENGTH_SHORT).show();
            }
        }).setPositiveButton("Send", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                Toast.makeText(getActivity(), "Remark "+remark.getText().toString(), Toast.LENGTH_SHORT).show();
                Toast.makeText(mActivity, fname, Toast.LENGTH_SHORT).show();


                if(selectedforward.equals("Forward to Employee")){

                    OkHttpHandler_forward okHttpHandler= new OkHttpHandler_forward();
                    okHttpHandler.execute(postUrl_get_dept_employees);

                }else{
                    OkHttpHandler okHttpHandler= new OkHttpHandler();
                    okHttpHandler.execute(postUrl_forward);

                }


                /*Reload Activity*/
                mActivity.finish();
                startActivity(mActivity.getIntent());
                /*Reload Activity*/
            }
        });

        return bd.create();
}



    class OkHttpHandler extends AsyncTask<String, String, String> {

        OkHttpClient client = new OkHttpClient();

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
           /* progressDialog = new ProgressDialog(getContext());
            progressDialog.setMessage("Forwarding");
            progressDialog.setCancelable(false);
            progressDialog.show();*/
        }

        @Override
        protected String doInBackground(String... params) {

            JSONObject barcodeTxt = new JSONObject();
            try {

                barcodeTxt.put("remark",remark.getText().toString());
                barcodeTxt.put("filename",fname);

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
            /*progressDialog.dismiss();*/

            try {
                String loginResponseString = response;
                Log.d("Forward Response", "Response from the server for files : " + loginResponseString);

                JSONObject result= new JSONObject(loginResponseString);

                if (result.getString("status").equals("1")) {
                    Toast.makeText(getContext(), "Forwarded Successfuly", Toast.LENGTH_SHORT).show();


                    /* startActivity(new Intent( getApplicationContext(), MainScanActivity.class));*/
                    // finish();//finishing activity and return to the calling activity.
                } else if (result.getString("status").equals("0")) {
                    Toast.makeText(getContext(), "Failed to send", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Failed to send");
                }else if(result.getString("status").equals("2")){
                    Toast.makeText(getContext(), "Method error", Toast.LENGTH_SHORT).show();
                    //responseTextLogin.setText("Method error");
                }else if(result.getString("status").equals("3")){
                    Toast.makeText(getContext(), "Database error", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Database error");
                }
            } catch (Exception e) {
                e.printStackTrace();
              //  Toast.makeText(mActivity.getApplicationContext(), "Something went wrong. Please try again later.", Toast.LENGTH_SHORT).show();

            }





        }
    }

    class OkHttpHandler_forward extends AsyncTask<String, String, String> {

        OkHttpClient client = new OkHttpClient();

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
           /* progressDialog = new ProgressDialog(getContext());
            progressDialog.setMessage("Forwarding");
            progressDialog.setCancelable(false);
            progressDialog.show();*/
        }

        @Override
        protected String doInBackground(String... params) {

            JSONObject barcodeTxt = new JSONObject();
            try {
                barcodeTxt.put("nextEmp","");
                barcodeTxt.put("remark",remark.getText().toString());
                barcodeTxt.put("filename",fname);

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
            /*progressDialog.dismiss();*/

            try {
                String loginResponseString = response;
                Log.d("Forward Response", "Response from the server for files : " + loginResponseString);

                JSONObject result= new JSONObject(loginResponseString);

                if (result.getString("status").equals("1")) {
                    Toast.makeText(getContext(), "Forwarded Successfuly", Toast.LENGTH_SHORT).show();


                    /* startActivity(new Intent( getApplicationContext(), MainScanActivity.class));*/
                    // finish();//finishing activity and return to the calling activity.
                } else if (result.getString("status").equals("0")) {
                    Toast.makeText(getContext(), "Failed to send", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Failed to send");
                }else if(result.getString("status").equals("2")){
                    Toast.makeText(getContext(), "Method error", Toast.LENGTH_SHORT).show();
                    //responseTextLogin.setText("Method error");
                }else if(result.getString("status").equals("3")){
                    Toast.makeText(getContext(), "Database error", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Database error");
                }
            } catch (Exception e) {
                e.printStackTrace();
                //  Toast.makeText(mActivity.getApplicationContext(), "Something went wrong. Please try again later.", Toast.LENGTH_SHORT).show();

            }





        }
    }

    class Get_dept_emails extends AsyncTask<String, String, String> {

        OkHttpClient client = new OkHttpClient();

        @Override
        protected void onPreExecute() {
            super.onPreExecute();

        }

        @Override
        protected String doInBackground(String... params) {



            Log.d("Dept ID", "------------------------------- : " +dept_id);

            HttpUrl mygetEmphUrl = new HttpUrl.Builder()
                    .scheme("https")
                    .host(const_posturl)
                    .addPathSegment("get_dept_employees")
                    .addQueryParameter("dept_id", dept_id)
                    .build();

            Request request = new Request.Builder()
                    .url(mygetEmphUrl)
                    .addHeader("Accept", "application/json")
                    .method("GET", null)
                    .build();

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
            /*progressDialog.dismiss();*/

            try {



                JSONObject result= new JSONObject(response);


                Log.d("Forward Response", "Response from the server for employee email : " + response);

                if (result.getString("status").equals("1")) {


                    JSONArray emp = result.getJSONArray("employees");

                    Log.d("EMploe+++++++", "Response  : " + emp);

                    Log.d("EMploe+++++++", "Response  : " + emp.length());


                    for(int i=0;i<emp.length();i++){
                        JSONObject emails= (JSONObject) emp.get(i);
                        String emailid = emails.getString("email_id");

                        Log.d("EMAIL", "Response________  : " + emailid);
                        mDept_emails.add(new Dept_emails(emailid));
                    }


                    email_spinner_adapter = new Email_Spinner_Adapter(getContext(), mDept_emails);
                    email_spin.setAdapter(email_spinner_adapter);

                    email_spin.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                        @Override
                        public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                            Dept_emails clickItem= (Dept_emails) parent.getItemAtPosition(position);
                            String clickedEmail = clickItem.getDept_emails();
                            //Toast.makeText(mActivity, clickedEmail, Toast.LENGTH_SHORT).show();

                            selectedNextEmail = clickedEmail;
                        }

                        @Override
                        public void onNothingSelected(AdapterView<?> parent) {

                        }
                    });

                    // finish();//finishing activity and return to the calling activity.
                } else if (result.getString("status").equals("0")) {
                    Toast.makeText(getContext(), "Failed to send", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Failed to send");
                }else if(result.getString("status").equals("2")){
                    Toast.makeText(getContext(), "Method error", Toast.LENGTH_SHORT).show();
                    //responseTextLogin.setText("Method error");
                }else if(result.getString("status").equals("3")){
                    Toast.makeText(getContext(), "Database error", Toast.LENGTH_SHORT).show();
                    // responseTextLogin.setText("Database error");
                }
            } catch (Exception e) {
                e.printStackTrace();
                //  Toast.makeText(mActivity.getApplicationContext(), "Something went wrong. Please try again later.", Toast.LENGTH_SHORT).show();

            }





        }
    }

}
