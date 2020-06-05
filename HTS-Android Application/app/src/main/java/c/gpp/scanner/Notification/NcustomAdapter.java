package c.gpp.scanner.Notification;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.ArrayList;

import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.RecyclerView;
import c.gpp.scanner.R;

public class NcustomAdapter extends RecyclerView.Adapter<NcustomAdapter.MyViewHolder> {

    ArrayList<NListPojo> listPojos;
    Context context;
    public NcustomAdapter(Context context, ArrayList listPojos) {
        this.context = context;
        this.listPojos = listPojos;

    }
    @Override
    public NcustomAdapter.MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        // infalte the item Layout
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.n_custom_list, parent, false);
        // set the view's size, margins, paddings and layout parameters
        NcustomAdapter.MyViewHolder vh = new NcustomAdapter.MyViewHolder(v); // pass the view to View Holder
        return vh;
    }
    @Override
    public void onBindViewHolder(NcustomAdapter.MyViewHolder holder, final int position) {
        // set the data in items
        holder.notificationId.setText(listPojos.get(position).getNotificationId());
        holder.msg.setText(listPojos.get(position).getMsg());
        holder.timeCreated.setText(listPojos.get(position).getTimeCreated());

        if(listPojos.get(position).getColor().equals("old")){

            int color = holder.notifyCard.getContext().getResources().getColor(R.color.old);
            holder.notifyCard.setCardBackgroundColor(color);
        }



    }
    @Override
    public int getItemCount() {
        return listPojos.size();
    }
    public class MyViewHolder extends RecyclerView.ViewHolder {
        // init the item view's
        TextView notificationId;
        TextView msg;
        TextView timeCreated;
        CardView notifyCard;

        public MyViewHolder(View itemView) {
            super(itemView);
            // get the reference of item view's
            notificationId = (TextView) itemView.findViewById(R.id.notification_id);
            msg = (TextView) itemView.findViewById(R.id.msg);
            timeCreated = (TextView) itemView.findViewById(R.id.timeCreated);
            notifyCard = itemView.findViewById(R.id.notifyCard);


        }
    }
}