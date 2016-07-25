package internetSnake;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketTimeoutException;


public class SnakeServer extends Thread{
	/*public static void main(String[] args) throws InterruptedException{
		while(true){
			System.out.println("newgame");
			Snake.startGame();
			Snake.gameCont = true;
		}		
	}*/
	private ServerSocket serverSocket;
	   
	public SnakeServer(int port) throws IOException{
		serverSocket = new ServerSocket(port);
		//serverSocket.setSoTimeout(100000);
	}

	public void run(){
		while(true){
			try{
				System.out.println("Waiting for client on port " + serverSocket.getLocalPort() + "...");
				Socket server = serverSocket.accept();
				System.out.println("Just connected to " + server.getRemoteSocketAddress());
            
		        //DataInputStream in = new DataInputStream(server.getInputStream());
		        //System.out.println(in.readUTF());
		        
		        DataOutputStream out = new DataOutputStream(server.getOutputStream());	
		        BufferedReader reader = new BufferedReader(new InputStreamReader(server.getInputStream()));
		        
		        System.out.println("we are now starting the game");
		        Snake.startGame(out, reader);
		        
		        
		        //DataInputStream in = new DataInputStream(server.getInputStream());
		        
		        
		        
		        
		        server.close();
			}catch(SocketTimeoutException s){
				System.out.println("Socket timed out!");
				break;
			}catch(IOException e){
				e.printStackTrace();
				break;
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	public static void main(String [] args){
	      int port = 6066;
	      try
	      {
	         Thread t = new SnakeServer(port);
	         t.start();
	      }catch(IOException e)
	      {
	         e.printStackTrace();
	      }
	   }
}
