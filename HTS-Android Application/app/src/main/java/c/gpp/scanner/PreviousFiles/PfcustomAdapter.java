package c.gpp.scanner.PreviousFiles;

import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import java.util.ArrayList;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.FragmentManager;
import androidx.recyclerview.widget.RecyclerView;
import c.gpp.scanner.CurrentFiles.ListPojo;
import c.gpp.scanner.CurrentFiles.MyRemarkFragment;
import c.gpp.scanner.R;

public class PfcustomAdapter extends RecyclerView.Adapter<PfcustomAdapter.MyViewHolder> {

    ArrayList<Pf_listpojo> listPojos;
    Context context;
    public PfcustomAdapter(Context context, ArrayList listPojos) {
        this.context = context;
        this.listPojos = listPojos;

    }
    @Override
    public PfcustomAdapter.MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        // infalte the item Layout
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.pf_customlist, parent, false);
        // set the view's size, margins, paddings and layout parameters
        PfcustomAdapter.MyViewHolder vh = new PfcustomAdapter.MyViewHolder(v); // pass the view to View Holder
        return vh;
    }
    @Override
    public void onBindViewHolder(PfcustomAdapter.MyViewHolder holder, final int position) {
        // set the data in items
        holder.fileid.setText(listPojos.get(position).getFileID());
        holder.delay.setText(listPojos.get(position).getDelay());
        holder.arrivaltime.setText(listPojos.get(position).getArrivaltime());

    }
    @Override
    public int getItemCount() {
        return listPojos.size();
    }
    public class MyViewHolder extends RecyclerView.ViewHolder {
        // init the item view's
        TextView fileid;
        TextView delay;
        TextView arrivaltime,completetime;

        public MyViewHolder(View itemView) {
            super(itemView);
            // get the reference of item view's
            fileid = (TextView) itemView.findViewById(R.id.fileid);
            delay = (TextView) itemView.findViewById(R.id.delay);
            arrivaltime = (TextView) itemView.findViewById(R.id.arrivaltime);
            completetime = (TextView) itemView.findViewById(R.id.completetime);

        }
    }
}