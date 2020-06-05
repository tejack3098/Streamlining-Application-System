package c.gpp.scanner.ArrivingFiles;

public class Aflistpojo {
    private String fileId;
    private  String remark;
    private String arrivaltime;
    private String key;
    private String from;
    private String time;
    private String alerted;

    public String getAlerted() {
        return alerted;
    }

    public void setAlerted(String alerted) {
        this.alerted = alerted;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getFrom() {
        return from;
    }

    public void setFrom(String from) {
        this.from = from;
    }

    public String getFileId() {
        return fileId;
    }

    public void setFileId(String fileId) {
        this.fileId = fileId;
    }

    public String getRemark() {
        return remark;
    }

    public void setRemark(String remark) {
        this.remark = remark;
    }

    public String getArrivaltime() {
        return arrivaltime;
    }

    public void setArrivaltime(String arrivaltime) {
        this.arrivaltime = arrivaltime;
    }

    public Aflistpojo(String fileId, String remark, String arrivaltime, String key ,String from, String time, String alerted) {
        this.fileId = fileId;
        this.remark = remark;
        this.arrivaltime = arrivaltime;
        this.key = key;
        this.from = from;
        this.time = time;
        this.alerted = alerted;
    }
}
