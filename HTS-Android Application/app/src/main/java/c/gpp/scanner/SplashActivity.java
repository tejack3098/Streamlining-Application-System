package c.gpp.scanner;


import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Handler;
import androidx.appcompat.app.AppCompatActivity;
import c.gpp.scanner.Home.MainScanActivity;
import c.gpp.scanner.Login.MainActivity;

import android.os.Bundle;

public class SplashActivity extends AppCompatActivity {
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);
        /*****************************************Shared pref************************************************/
        saved = getApplicationContext().getSharedPreferences("shared_pref", Context.MODE_PRIVATE);
        saved_edit = saved.edit();
        /*****************************************Shared pref************************************************/
        new Handler().postDelayed(new Runnable() {


            @Override
            public void run() {
                // This method will be executed once the timer is over
                Intent i;
                if(!saved.contains("logged_in"))
                {
                    
                    saved_edit.putInt("logged_in",0);
                    saved_edit.apply();
                }
                if (saved.getInt("logged_in",0)==0)
                {
                    i = new Intent(SplashActivity.this, MainActivity.class);
                }
                else
                {
                    i = new Intent(SplashActivity.this, MainScanActivity.class);
                }

                startActivity(i);
                finish();
            }
        }, 3000);
    }
}

