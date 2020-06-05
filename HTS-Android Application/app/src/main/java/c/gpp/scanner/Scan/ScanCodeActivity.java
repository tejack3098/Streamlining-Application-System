package c.gpp.scanner.Scan;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import com.google.zxing.Result;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import androidx.appcompat.app.AppCompatActivity;
import c.gpp.scanner.ArrivingFiles.ArrivingFilesActivity;
import c.gpp.scanner.Home.MainScanActivity;
import me.dm7.barcodescanner.zxing.ZXingScannerView;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static c.gpp.scanner.Login.MainActivity.postUrl;

public class ScanCodeActivity extends AppCompatActivity implements ZXingScannerView.ResultHandler {

    ZXingScannerView ScannerView;
    public static String bcode;
    static String postUrl2 = postUrl+ "/bcode_entry";
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        ScannerView = new ZXingScannerView(this);
        setContentView(ScannerView);

        /*****************************************Shared pref************************************************/
        saved = getApplicationContext().getSharedPreferences("shared_pref", Context.MODE_PRIVATE);
        saved_edit = saved.edit();
        /*****************************************Shared pref************************************************/
    }

    @Override
    public void handleResult(Result result) {

      //  MainScanActivity.tv.setText(result.getText());
        bcode=result.getText();
        Submit();
        onBackPressed();

    }

    @Override
    protected void onPause() {
        super.onPause();

        ScannerView.stopCamera();
    }

    @Override
    protected void onResume() {
        super.onResume();

        ScannerView.setResultHandler(this);
        ScannerView.startCamera();
    }

    public void Submit() {


        JSONObject barcodeTxt = new JSONObject();

        try {
            Toast.makeText(this,ScanCodeActivity.bcode, Toast.LENGTH_SHORT).show();
            String btx = bcode;
        /*     barcodeTxt.put("email",MainActivity.email);
            barcodeTxt.put("deptID", MainActivity.depId);
            barcodeTxt.put("bcodeTxt", btx);*/
            barcodeTxt.put("email",saved.getString("email","NULL"));
            barcodeTxt.put("bcodeTxt", btx);
            barcodeTxt.put("deptID", saved.getString("dept_id","NULL"));

        } catch (JSONException e) {
            e.printStackTrace();
        }

        RequestBody body = RequestBody.create(MediaType.parse("application/json; charset=utf-8"), barcodeTxt.toString());

        postRequest(postUrl2, body);
    }

    public void postRequest(String postUrl, RequestBody postBody) {
        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url(postUrl)
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
                        Toast.makeText(ScanCodeActivity.this, "Failed to Connect to Server. Please Try Again.", Toast.LENGTH_SHORT).show();
                    }
                });
            }

            @Override
            public void onResponse(Call call, final Response response) throws IOException {
                // In order to access the TextView inside the UI thread, the code is executed inside runOnUiThread()
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            String loginResponseString = response.body().string().trim();
                            Log.d("LOGIN", "Response from the server : " + loginResponseString);

                            JSONObject result= new JSONObject(loginResponseString);

                            if (result.getString("status").equals("1")) {
                                Log.d("LOGIN", "Successfull Login");
                                Toast.makeText(ScanCodeActivity.this, "Send Successfuly", Toast.LENGTH_SHORT).show();
                                startActivity(new Intent( getApplicationContext(), MainScanActivity.class));
                                 finish();//finishing activity and return to the calling activity.
                            } else if (result.getString("status").equals("0")) {
                                Toast.makeText(ScanCodeActivity.this, "Failed to send", Toast.LENGTH_SHORT).show();
                                // responseTextLogin.setText("Failed to send");
                            }else if(result.getString("status").equals("2")){
                                Toast.makeText(ScanCodeActivity.this, "Method error", Toast.LENGTH_SHORT).show();
                                //responseTextLogin.setText("Method error");
                            }else if(result.getString("status").equals("3")){
                                Toast.makeText(ScanCodeActivity.this, "Database error", Toast.LENGTH_SHORT).show();
                                // responseTextLogin.setText("Database error");
                            }
                        } catch (Exception e) {
                            e.printStackTrace();
                            Toast.makeText(ScanCodeActivity.this, "Something went wrong. Please try again later.", Toast.LENGTH_SHORT).show();

                        }
                    }
                });
            }
        });
    }

}

