import java.io.*;
import org.json.*;
import java.util.*;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.CharacterData;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import org.xml.sax.InputSource;
import java.lang.*;
/*
 * This class provides the functionality to process the corpus data for SemEval 2015 Task 4 Track B. It processees the data in each corpus using the TWC + W2C 0010 model
 */
public class TWCW2V0010 {
	
		 /**
		 * @param args
		 */
		//Set of target entities
		public Set <String> corpusTopics = new HashSet<String>();
		public static final int INDENT_FACTOR=4;
		//directory for source data
		public static String dataDir;
		
		//directory for log file. Created in the same directory as source directory
		public static String logFileName;
		
		//Assume the dataDir has a list of corpus directories. 
		//Loop thru each corpus directory and load the target entities into a set for each corpus
		//input to program is a target entity
		//if input is not in the corpus set, error out
		//if it is in target set, then process
		public   TWCW2V0010(String sourceDir, String logFile) {
			
			dataDir = sourceDir;
			logFileName = logFile;
			
			//CORPUS 1
			//loadTargetEntities ("corpus_1");
			processTimeMLFiles("corpus_1");
			//loadGoldEvents ("corpus_1");
			//CORPUS 2
			//loadTimeMLFiles("corpus_2");
			//loadGoldEvents ("corpus_2");
			//loadTargetEntities ("corpus_2");
			//System.out.println(corpusTopics.size());
			//CORPUS 3
			//loadTimeMLFiles("corpus_3");
			//loadGoldEvents ("corpus_3");
			//loadTargetEntities ("corpus_3");
			//System.out.println(corpusTopics.size());
			
		}
		//loads all the gold time line files into a json array. Each file is loaded into a JSON object.
		private void loadGoldEvents (String corpusName){
			JSONObject fileJSON = null;
			File GoldDir = new File (dataDir+ "/" + corpusName+ "/TimeLines_Gold_Standard");
			 List <JSONObject> jsonGoldArray = new ArrayList <JSONObject> ();
			 if(GoldDir.isDirectory()) {
				 //get list of Gold files in the directory
				 File [] files = GoldDir.listFiles();
				 				 
				 for (int i= 0;i< files.length;i++) {
					 //read first line as tag name
					 fileJSON = createJSONFromFile(files[i]);
					 fileJSON.toString(4);
					 jsonGoldArray.add(createJSONFromFile(files[i]));
					 //System.out.println("File Content" + i+ ":-" + jsonGoldArray.get(i).toString(4));
							
					}
					 //subsequent lines are gold events
				 
			 } 
			 else System.out.println("Invalid Path: Not a directory for Gold Event files");
			
		}
		
		//returns a JSON object from a gold event file
		private JSONObject createJSONFromFile(File file) {
			JSONObject goldJSON = new JSONObject();
			//JSONArray eventJSONArray = new JSONArray(); 
			
			 try {
				 	BufferedReader in = new BufferedReader(
					new InputStreamReader( new FileInputStream(file), "UTF8"));
				 	
				 					
				 	String fileLine;
					String key;
					//temporary object to store event JSON
					JSONObject eJSON = null;
					
					//counter to count lines in file [. first line is the target entity 
					int lnNumber =1;
					
					//this loop reads thru the lines in the GOLD Event file and creates a JSON object from the contents of the file. 
					//It assumes a certain format
					while ((fileLine = in.readLine()) != null) {
					   // System.out.println(fileLine);
					    if (lnNumber == 1) {
					    	key = "Entity";
					    	goldJSON.put(key, fileLine );
					    	//System.out.println("First Line:- " + goldJSON.toString(4));
					     }
					    else {
					    	//convert the event mentions to JSON objects and form an array
					    	//key = "GoldTimeLine";
					    	eJSON = convertToEventJSON(fileLine);
					    	key = "TimeLine";
							goldJSON.append(key, eJSON); 
							//System.out.println("No of Objects in array:-" + goldJSON.length());
					 
	
					    }
					   					   
					    lnNumber++;
					   
					   //System.out.println(goldJSON.toString(4));
					}
					//System.out.println("Before adding array:-" + goldJSON.toString(4));
					/*
					key = "TimeLine";
					goldJSON.put(key, eventJSONArray); 
					
				    */in.close();
			 	}
			    catch (UnsupportedEncodingException e)
			    {
					System.out.println(e.getMessage());
			    }
			    catch (IOException e)
			    {
					System.out.println(e.getMessage());
			    }
			 	catch (JSONException je) {
			 		 throw new RuntimeException(je);
			 	}
			    catch (Exception e)
			    {
					System.out.println(e.getMessage());
			    }
			
			return goldJSON;
		}
		
		//method to form a JSON object from each TimLine row in file
		private JSONObject convertToEventJSON( String eventLine) {
			String [] eventStr = eventLine.split("\\t");
			//System.out.println(eventStr[0] + "--" + eventStr[1] + "--" + eventStr[2]);
			JSONObject eventJSON = new JSONObject();
			String key;
			key = "order";
			eventJSON.put(key, eventStr[0]);
			key = "time";
			eventJSON.put(key, eventStr[1]);
			key = "events";
			eventJSON.put(key, eventStr[2]);
			return eventJSON;
		} 
		
	
		private void processTimeMLFiles(String corpusName) {
			File TimeMLDir = new File (dataDir+ "/" + corpusName+ "/corpus_trackB_TimeML");
			JSONObject fileJson = null;
			
			try {
			
				File outFile = new File(dataDir + "/output/"+ corpusName + "_output.txt");
				
				//delete the output file if it exists
				if (outFile.exists()) outFile.delete();
				
				Writer out = new BufferedWriter(new OutputStreamWriter( new FileOutputStream(outFile), "UTF8"));
				
				 if(TimeMLDir.isDirectory()) {
					 //get list of TimeML files in the directory
					 File [] files = TimeMLDir.listFiles();
					 
					 //output the TEXT element from the timeML files
					 
					 for (int i= 0;i< files.length;i++) {
						
						 //processTMLFile(files[i]);
						 
						 fileJson = processTMLFile(files[i]);
						 out.append(fileJson.toString()+ System.lineSeparator());
						 System.out.println("File written: " + files[i].getName());
						 /* if (i< 2) {
							  fileJson = processTMLFile(files[i]);
							  out.append(fileJson.toString()+ System.lineSeparator());
							  System.out.println("File written: " + files[i].getName());
						  }*/
					 }		 
				 }
				 else System.out.println("Invalid Path: Not a directory for TimeML files");
				 out.flush();
				 out.close();
			}
			catch (Exception e) {
				 e.printStackTrace(); 
			}
			
		}
		//parsing and reading TimeML files to JSON
		private JSONObject processTMLFile (File file) {
			JSONObject jsonObj = null;
			try { 
				
				
				DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance(); 
	            InputStream inputStream = new FileInputStream(file); 
	            //read as UTF-8
	            org.w3c.dom.Document doc = documentBuilderFactory.newDocumentBuilder().parse(inputStream, "UTF-8"); 
	            
	            StringWriter stw = new StringWriter(); 
	            Transformer serializer = TransformerFactory.newInstance().newTransformer(); 
	            serializer.transform(new DOMSource(doc), new StreamResult(stw)); 
	           
	           
	            jsonObj = XML.toJSONObject(stw.toString(), true);  
	          
	           //get the text as its own object
	            String rawText = getRawTextFromXml(stw.toString());
	            jsonObj.accumulate("RAW TEXT", rawText);

	            JSONObject tipSem = XML.toJSONObject(getTIPSemOutput(rawText));
	            //add Tipsem output to JSON String
	            jsonObj.put("TIPSEM", tipSem);
	            //System.out.println(jsonObj.toString(3));
	           
	            //add opeNER output
	            //String cmdout = getOpeNERCData(rawText);
	            //JSONObject tmpJSON = new JSONObject("{" + cmdout + "}");
	            //System.out.println(cmdout);
	            //jsonObj.put("OPENER",tmpJSON);
	            System.out.println(jsonObj.toString(3));
		        
	            
	            //get word2vec scores
	            //String cmdout = getWord2VecInfo(rawText);
	            
	            
	         
			}
	         catch(IOException ex) {
	                System.out.println(
	                    "Error writing to file '"
	                    + file + "'");
	                // Or we could just do this:
	                // ex.printStackTrace();
	         } catch(Exception e) {  
	                e.printStackTrace();  
	            }
			return jsonObj;
	    }
	private String getWord2VecInfo(String rawText) {
		String str = "";
		String cmdArray[] = {"python", "/home/osboxes/getannotations.py", rawText};
		String cmdOutput = runCommand(cmdArray);
		return cmdOutput;
	}
	private String getOpeNERCData(String rawText) {
			//String cmdArray []= {"curl", "-d", "\"@-\"","http://opener.olery.com/language-identifier", "<<<",  "\"input="+ rawText + "\""};
			String cmdArray []= {"/home/osboxes/ML/TCW2V0010/getOpeNEROutput.sh", rawText};
			//System.out.println(cmdArray[0] + cmdArray[1]);
			String cmdOutput = "";
			// process the raw text thru the whole pipeline
			
			//first get the language identifier
			cmdOutput = runCommand(cmdArray);
			
			return cmdOutput;
		}
		private String getTIPSemOutput(String rawText) {
			String tipSemOutput = "";
			try {
				//the command and its params should be passed as a string array 
	            //with first element as the command
	            String cmdArray [] = {"java", "-jar", "/home/osboxes/ML/otip-master/target/tipsem-1.0.0.jar", "-t", rawText};
	             tipSemOutput = runCommand (cmdArray);
	        
			} 
			catch (Exception e) {
				e.printStackTrace();
			}
			    return tipSemOutput;
			
		}
		private String getRawTextFromXml(String stw) {
			String textString = "";
			try {
				Document doc;
				DocumentBuilderFactory fctr = DocumentBuilderFactory.newInstance();
				DocumentBuilder bldr = fctr.newDocumentBuilder();
				InputSource insrc = new InputSource(new StringReader(stw));
				doc =  bldr.parse(insrc);
			
				//Node txtElement = doc.getElementsByTagName("TEXT").item(0);
				//System.out.println(txtElement.getTextContent());
				textString = "";
				NodeList sentenceList = doc.getElementsByTagName("s");
				//first two sentence elements are the title and the date of the document. so ignore them
				 for (int s = 2; s < sentenceList.getLength();s++ ) {
					 if (s==2) textString += sentenceList.item(s).getTextContent(); else textString += " " + sentenceList.item(s).getTextContent();
					 //System.out.println(sentenceList.item(s).getTextContent());
					 					
				}
				//System.out.println(textString);
			}
			catch (Exception e) {
				System.out.println("Error generating raw text");
			}
			
			return textString;
		}
		//This functions runs a shell command and returns output from cammand as string
		private String runCommand (String[] command) {

			//System.out.println(command[0]);
			StringBuilder output = new StringBuilder();

			Process proc;
			try {
				proc = Runtime.getRuntime().exec(command);
				proc.waitFor();
				BufferedReader reader =
	                            new BufferedReader(new InputStreamReader(proc.getInputStream()));

	                        String line = reader.readLine();
	                        
	            System.out.println(line);
				while ((line = reader.readLine())!= null) {
					//System.out.println(line);
					output.append(line + "\n");
				}

			} catch (Exception e) {
				e.printStackTrace();
			}

			return output.toString();

		}
						
		
	}
