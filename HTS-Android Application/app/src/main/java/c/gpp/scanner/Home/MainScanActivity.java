package c.gpp.scanner.Home;

import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import c.gpp.scanner.ArrivingFiles.ArrivingFilesActivity;
import c.gpp.scanner.CurrentFiles.CurFilesActivity;
import c.gpp.scanner.Notification.NotificationActivity;
import c.gpp.scanner.PreviousFiles.PreviousFilesActivity;
import c.gpp.scanner.EmpStats.EmpStatsActivity;
import c.gpp.scanner.Login.MainActivity;
import c.gpp.scanner.R;

import android.app.Notification;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;


public class MainScanActivity extends AppCompatActivity {
    private SharedPreferences saved;
    private SharedPreferences.Editor saved_edit;
    TextView Emptv;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_scan);

        Emptv = findViewById(R.id.Gridtitle);

        final CardView arrFilesCard = (CardView) findViewById(R.id.scanCard);
        final CardView curFilesCard = (CardView) findViewById(R.id.curFilesCard);
        final CardView prevFilesCard = (CardView) findViewById(R.id.prevFilesCard);
        final Button logoutBtn = (Button) findViewById(R.id.logoutbtn);
        final ImageView notificationBtn =  findViewById(R.id.notificationbtn);
        final CardView empStatsCard = (CardView) findViewById(R.id.emp_statsCard);
        /*****************************************Shared pref************************************************/
        saved = getApplicationContext().getSharedPreferences("shared_pref", Context.MODE_PRIVATE);
        saved_edit = saved.edit();
        /*****************************************Shared pref************************************************/

        Emptv.setText(saved.getString("email", "NULL"));

        arrFilesCard.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), ArrivingFilesActivity.class));
            }
        });

        curFilesCard.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), CurFilesActivity.class));
            }
        });

        prevFilesCard.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), PreviousFilesActivity.class));
            }
        });


        empStatsCard.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), EmpStatsActivity.class));

            }
        });

        notificationBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivity(new Intent(getApplicationContext(), NotificationActivity.class));
            }
        });

        logoutBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saved_edit.putInt("logged_in", 0);
                saved_edit.apply();
                startActivity(new Intent(getApplicationContext(), MainActivity.class));
                finish();
            }
        });

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.option_menu, menu);
        return true;
    }



    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch ((item.getItemId())) {

            case R.id.login_btn:
                saved_edit.putInt("logged_in", 0);
                saved_edit.apply();
                startActivity(new Intent(getApplicationContext(), MainActivity.class));
                finish();

            default:
                return super.onOptionsItemSelected(item);
        }
    }
}
