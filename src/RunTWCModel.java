import java.util.*;
public class RunTWCModel {

	/**
	 * @param args
	 */
	
	public static void main(String[] args) {
		String dataDir = "/home/osboxes/ML/semeval-2015-task-4-master"; 
		//log file name to log progress and errors
		String logFile = "getResults.log";

		// TODO Auto-generated method stub
		TWCW2V0010 t = new TWCW2V0010(dataDir, logFile);
		//access via Iterator
		Iterator<String> itr = t.corpusTopics.iterator();
		while(itr.hasNext()){
		  System.out.println( itr.next());
		}
		//System.out.println(t.corpusTopics.size());

	}

}
