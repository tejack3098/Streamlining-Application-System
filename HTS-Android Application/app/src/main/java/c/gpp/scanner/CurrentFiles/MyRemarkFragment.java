package c.gpp.scanner.CurrentFiles;


import android.annotation.SuppressLint;
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
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import c.gpp.scanner.R;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.IOException;
import static c.gpp.scanner.Login.MainActivity.postUrl;


/**
 * A simple {@link Fragment} subclass.
 */
public class MyRemarkFragment extends DialogFragment {

    static String postUrl_forward = postUrl+ "/forward";
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    EditText remark;
    String fname;
    private Activity mActivity;
    ProgressDialog progressDialog;

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

        Bundle bundle = getArguments();
        fname = bundle.getString("fname","");



        AlertDialog.Builder bd = new AlertDialog.Builder(getActivity());
        LayoutInflater inflater = getActivity().getLayoutInflater();

        View DialogView = inflater.inflate(R.layout.fragment_my_remark,null);

       remark = DialogView.findViewById(R.id.remark);


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

                OkHttpHandler okHttpHandler= new OkHttpHandler();
                okHttpHandler.execute(postUrl_forward);

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



}
