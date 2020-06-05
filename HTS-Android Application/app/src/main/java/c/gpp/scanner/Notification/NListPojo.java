package c.gpp.scanner.Notification;

public class NListPojo {


    private  String notificationId;
    private  String msg;
    private String timeCreated;
    private String color;

    public NListPojo(String notificationId, String msg, String timeCreated,String color) {
        this.notificationId = notificationId;
        this.msg = msg;
        this.timeCreated = timeCreated;
        this.color = color;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public String getNotificationId() {
        return notificationId;
    }

    public void setNotificationId(String notificationId) {
        this.notificationId = notificationId;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public String getTimeCreated() {
        return timeCreated;
    }

    public void setTimeCreated(String timeCreated) {
        this.timeCreated = timeCreated;
    }
}
