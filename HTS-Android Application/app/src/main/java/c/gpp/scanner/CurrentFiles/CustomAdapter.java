package c.gpp.scanner.CurrentFiles;

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
import c.gpp.scanner.R;

public class CustomAdapter extends RecyclerView.Adapter<CustomAdapter.MyViewHolder>  {
    ArrayList<ListPojo> listPojos;

    Context context;
    public CustomAdapter(Context context, ArrayList listPojos) {
        this.context = context;
        this.listPojos = listPojos;

    }
    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        // infalte the item Layout
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.custom_list, parent, false);
        // set the view's size, margins, paddings and layout parameters
        MyViewHolder vh = new MyViewHolder(v); // pass the view to View Holder
        return vh;
    }
    @Override
    public void onBindViewHolder(MyViewHolder holder, final int position) {
        // set the data in items
        holder.fileid.setText(listPojos.get(position).getFileID());
        holder.delay.setText(listPojos.get(position).getDelay());
        holder.arrivaltime.setText(listPojos.get(position).getArrivaltime());

        holder.forwardbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                FragmentManager manager = ((AppCompatActivity)context).getSupportFragmentManager();

                Bundle bundle = new Bundle(); //Bundle containing data you are passing to the dialog
                bundle.putString("fname", listPojos.get(position).getFileID());
                MyRemarkFragment remarkFragment = new MyRemarkFragment();
                remarkFragment.setArguments(bundle);
                remarkFragment.show(manager,"MyRemarkFragment");
            }
        });




    }
    @Override
    public int getItemCount() {
        return listPojos.size();
    }
    public class MyViewHolder extends RecyclerView.ViewHolder {
        // init the item view's
        TextView fileid;
        TextView delay;
        TextView arrivaltime;
        Button forwardbtn;

        public MyViewHolder(View itemView) {
            super(itemView);
            // get the reference of item view's
            fileid = (TextView) itemView.findViewById(R.id.fileid);
            delay = (TextView) itemView.findViewById(R.id.delay);
            arrivaltime = (TextView) itemView.findViewById(R.id.arrivaltime);
            forwardbtn = (Button) itemView.findViewById(R.id.forwardbtn);

        }
    }
}