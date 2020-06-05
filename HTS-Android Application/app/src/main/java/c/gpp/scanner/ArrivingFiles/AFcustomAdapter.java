package c.gpp.scanner.ArrivingFiles;

import android.app.ProgressDialog;
import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import androidx.recyclerview.widget.RecyclerView;
import c.gpp.scanner.R;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static c.gpp.scanner.ArrivingFiles.ArrivingFilesActivity.postUrl_notify;

public class AFcustomAdapter extends RecyclerView.Adapter<AFcustomAdapter.MyViewHolder> {
    ArrayList<Aflistpojo> listPojos;


    Context context;
    public AFcustomAdapter(Context context, ArrayList listPojos) {
        this.context = context;
        this.listPojos = listPojos;

    }
    @Override
    public AFcustomAdapter.MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        // infalte the item Layout
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.af_customlist, parent, false);
        // set the view's size, margins, paddings and layout parameters
        AFcustomAdapter.MyViewHolder vh = new AFcustomAdapter.MyViewHolder(v); // pass the view to View Holder
        return vh;
    }


    @Override
    public void onBindViewHolder(final AFcustomAdapter.MyViewHolder holder, final int position) {
        // set the data in items
        holder.fileid.setText(listPojos.get(position).getFileId());
        holder.remark.setText(listPojos.get(position).getRemark());
        holder.arrivaltime.setText(listPojos.get(position).getArrivaltime());

        if(listPojos.get(position).getAlerted().equals("true")){
            holder.alertbtn.setEnabled(false);
            holder.alertbtn.setText("Alerted");
        }else {

            holder.alertbtn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    AlertHandler alertHandler = new AlertHandler(context, listPojos.get(position).getKey(), listPojos.get(position).getFrom(), listPojos.get(position).getTime());
                    alertHandler.execute(postUrl_notify);
                    holder.alertbtn.setText("Alerted");
                }
            });
        }


    }
    @Override
    public int getItemCount() {
        return listPojos.size();
    }
    public class MyViewHolder extends RecyclerView.ViewHolder {
        // init the item view's
        TextView fileid;
        TextView remark;
        TextView arrivaltime;
        Button alertbtn;


        public MyViewHolder(View itemView) {
            super(itemView);
            // get the reference of item view's
            fileid = (TextView) itemView.findViewById(R.id.fileid);
            remark = (TextView) itemView.findViewById(R.id.remark);
            arrivaltime = (TextView) itemView.findViewById(R.id.arrivaltime);
            alertbtn = itemView.findViewById(R.id.alertbtn);

        }
    }


}
