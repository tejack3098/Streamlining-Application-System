package c.gpp.scanner.CurrentFiles;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.ArrayList;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import c.gpp.scanner.R;

public class Email_Spinner_Adapter extends ArrayAdapter<Dept_emails> {

    public  Email_Spinner_Adapter(Context context, ArrayList<Dept_emails> emails_list){
        super(context,0,emails_list);
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        return initView(position, convertView, parent);
    }

    @Override
    public View getDropDownView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        return initView(position, convertView, parent);
    }

    private View initView(int position, View convertView, ViewGroup parent){
        if(convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(
                    R.layout.dept_email_spinner_row, parent, false
            );
        }

            TextView email_tv = convertView.findViewById(R.id.dept_email_tv);

            Dept_emails d_email = getItem(position);

            if(d_email != null){
                email_tv.setText(d_email.getDept_emails());
            }

            return  convertView;

    }
}
