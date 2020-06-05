package c.gpp.scanner.Login;

import androidx.appcompat.app.AppCompatActivity;
import c.gpp.scanner.Home.MainScanActivity;
import c.gpp.scanner.R;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;


public class MainActivity extends AppCompatActivity {

    EditText emailView;
    EditText passView;
    Button login_btn;
    public String fname;
    public String lname;
    public static String depId;
    public static String email;
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    public static String postUrl = "http://84a35fb1.ngrok.io";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        emailView = (EditText) findViewById(R.id.email);
        passView = (EditText) findViewById(R.id.pass);
        login_btn = (Button)findViewById(R.id.login_btn);

        //startActivity(new Intent( getApplicationContext(), MainScanActivity.class));
        /*****************************************Shared pref************************************************/
        saved = getApplicationContext().getSharedPreferences("shared_pref", Context.MODE_PRIVATE);
        saved_edit = saved.edit();
        /*****************************************Shared pref************************************************/
    }

    public void Submit(View view) {

        String email = emailView.getText().toString().trim();
        String pass = passView.getText().toString().trim();

        if(email.length()==0 || pass.length()==0){
            Toast.makeText(this, "Please provide Email and Password", Toast.LENGTH_LONG).show();
        }

        JSONObject loginForm = new JSONObject();
        try {
            loginForm.put("subject", "login");
            loginForm.put("email", email);
            loginForm.put("pass", pass);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        RequestBody body = RequestBody.create(MediaType.parse("application/json; charset=utf-8"), loginForm.toString());

        postRequest(postUrl, body);
    }

    public void postRequest(String postUrl, RequestBody postBody) {
        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url(postUrl+"/emp_login")
                .post(postBody)
                .header("Accept", "application/json")
                .header("Content-Type", "application/json")
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                // Cancel the post on failure.
                call.cancel();
                Log.d("FAIL", e.getMessage());

                // In order to access the TextView inside the UI thread, the code is executed inside runOnUiThread()
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        TextView responseTextLogin = findViewById(R.id.resp);
                        responseTextLogin.setText("Failed to Connect to Server. Please Try Again.");
                    }
                });
            }

            @Override
            public void onResponse(Call call, final Response response) throws IOException {
                // In order to access the TextView inside the UI thread, the code is executed inside runOnUiThread()
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        TextView responseTextLogin = findViewById(R.id.resp);
                        try {
                            String loginResponseString = response.body().string().trim();
                            Log.d("LOGIN", "Response from the server : " + loginResponseString);

                            JSONObject result= new JSONObject(loginResponseString);

                           if (result.getString("status").equals("1")) {
                                Log.d("LOGIN", "Successful Login");
                                Toast.makeText(MainActivity.this, "Login Successfull", Toast.LENGTH_SHORT).show();

                               JSONObject msg  = result.getJSONObject("message");
                               fname = msg.getString("fname");
                               lname = msg.getString("lname");
                               depId = msg.getString("dept_id");
                               email = msg.getString("email");

                               saved_edit.putInt("logged_in",1);
                               saved_edit.putString("fname",fname);
                               saved_edit.putString("lname",lname);
                               saved_edit.putString("email",email);
                               saved_edit.putString("dept_id",depId);
                               saved_edit.apply();
                               startActivity(new Intent( getApplicationContext(), MainScanActivity.class));
                               finish();//finishing activity and return to the calling activity.
                            } else if (result.getString("status").equals("0")) {
                                responseTextLogin.setText("Login Failed. Invalid username or password.");
                            }else if(result.getString("status").equals("2")){
                                responseTextLogin.setText("Method error");
                           }else if(result.getString("status").equals("3")){
                               responseTextLogin.setText("Method error");
                           }
                        } catch (Exception e) {
                            e.printStackTrace();
                            responseTextLogin.setText("Something went wrong. Please try again later.");
                        }
                    }
                });
            }
        });
    }



}
