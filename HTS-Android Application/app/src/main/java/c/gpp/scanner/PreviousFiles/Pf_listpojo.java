package c.gpp.scanner.PreviousFiles;

public class Pf_listpojo {

    private  String fileID;
    private  String delay;
    private String arrivaltime;
    private String completetime;


    public String getCompletetime() {
        return completetime;
    }

    public void setCompletetime(String completetime) {
        this.completetime = completetime;
    }

    public String getFileID() {
        return fileID;
    }

    public String getDelay() {
        return delay;
    }

    public String getArrivaltime() {
        return arrivaltime;
    }

    public Pf_listpojo(String fileID, String delay, String arrivaltime, String completetime) {
        this.fileID = fileID;
        this.delay = delay;
        this.arrivaltime = arrivaltime;
        this.completetime = completetime;
    }
}
