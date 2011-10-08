/**
 * MechMania HTTP Interface
 * 
 * Aids in abstracting some of the craziness involved in making HTTP requests
 * in Java
 * 
 */

package edu.uiuc.acm.mechmania;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MechManiaHTTPInterface {
	private String serverHost;
	private int serverPort;
	
	public MechManiaHTTPInterface(String serverHost, int serverPort) {
		this.serverHost = serverHost;
		this.serverPort = serverPort;
	}

	/**
	 * Convenience signature for larger implementation below
	 * @param path Path to resource on server
	 */
	public URL buildRequestURL(String path) {
		return buildRequestURL(path, null);
	}
	
	/**
	 * Builds a request URL to a resource on a server
	 * 
	 * @param path Path to resource on server
	 * @param arguments Any GET arguments that might be necessary, passed as
	 *        "name=value" in an array of strings
	 * @return a URL object
	 */
	public URL buildRequestURL(String path, String[] arguments) {
		URL returnVal = null;
		String uriPath = path;
		
		if (arguments != null && arguments.length > 0) {
			uriPath = uriPath + "?";
			for (int i = 0; i < arguments.length; i++) {
				uriPath = uriPath + arguments[i];
				if (i < arguments.length - 1) {
					uriPath = uriPath + "&";
				}
			}
		}
		
		try {
			returnVal = new URL("http", serverHost, serverPort, uriPath);
		} catch (MalformedURLException e) {
			e.printStackTrace();
		}
		return returnVal;
	}
	
	/**
	 * Convenience signature for larger implementation below
	 * @param requestURL URL to be requested, generate using buildRequestURL()
	 * @return JSONObject containing the JSON response from the game server
	 */
	public JSONObject getResponse(URL requestURL) {
		return getResponse(requestURL, null);
	}
	
	/**
	 * Makes HTTP request, fetches response from server
	 * @param requestURL URL to be requested, generate using buildRequestURL()
	 * @param postData JSONObject containing any outgoing post data that changes the game state
	 * @return JSONObject containing the JSON response from the game server
	 */
	public JSONObject getResponse(URL requestURL, JSONObject postData) {
		String data = "";
		JSONObject returnJSON = null;
		BufferedReader responseBuffer;
		BufferedWriter postDataBuffer;
		URLConnection connection = null;
		try {
			connection = requestURL.openConnection();
			connection.setDoOutput(true);
			if (postData != null) {
				String postString = postData.toString();
				connection.setRequestProperty("Content-Length", ""+postString.length());
				postDataBuffer = new BufferedWriter(new OutputStreamWriter(connection.getOutputStream()));
				postDataBuffer.write(postString);
				postDataBuffer.flush();
				postDataBuffer.close();
			}
			HttpURLConnection urlConn = (HttpURLConnection) connection;
			if (urlConn.getResponseCode() == 200) {
				responseBuffer = new BufferedReader(new InputStreamReader(urlConn.getInputStream()));
			}
			else {
				responseBuffer = new BufferedReader(new InputStreamReader(urlConn.getErrorStream()));
			}
			data = responseBuffer.readLine();
			System.out.println(data);
			if (data.startsWith("{")) {
				returnJSON = new JSONObject(data);
			}
			else {
				JSONArray array = new JSONArray(data);
				returnJSON = new JSONObject();
				returnJSON.append("response", array);
			}
		} catch (IOException e) {
			e.printStackTrace();
		} catch (JSONException e) {
			e.printStackTrace();
		}
	
		return returnJSON;
	}
}
