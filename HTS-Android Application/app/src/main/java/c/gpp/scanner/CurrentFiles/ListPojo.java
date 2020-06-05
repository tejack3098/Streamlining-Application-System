package c.gpp.scanner.CurrentFiles;

public class ListPojo {

    private  String fileID;
    private  String delay;
    private String arrivaltime;




    public String getFileID() {
        return fileID;
    }

    public String getDelay() {
        return delay;
    }

    public String getArrivaltime() {
        return arrivaltime;
    }

    public ListPojo(String fileID, String delay, String arrivaltime) {
        this.fileID = fileID;
        this.delay = delay;
        this.arrivaltime = arrivaltime;
    }



}
