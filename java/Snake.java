package internetSnake;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.geom.Ellipse2D;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;

import javax.swing.JFrame;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class Snake extends JPanel /*implements ActionListener*/{
	
	//variables for Window
	private final static int W_HEIGHT = 700;
	private final static int B_DIMEN = 600;
	
	//game setting
	private final static int DELAY = 50;
	private final static int BLOCKSIZE = 40;
	private final static int INITLOCIX = BLOCKSIZE*3;
	private final static int INITLOCIY = BLOCKSIZE*3;
	private final static int POSITIONS = B_DIMEN/BLOCKSIZE;
	
	// for Snake
	private static int x[] = new int[POSITIONS*POSITIONS];
	private static int y[] = new int[POSITIONS*POSITIONS];
	
	// for apple
	private static int appleX;
	private static int appleY;
	
	//in game stuff
	public static boolean gameCont = true;
	private static Integer score = 0;
	private static String sscore;
	//private static String movementCount;
	private static int snakeLen = 3;
	//private static boolean pause = false;
	private static int timeFromApple = 0;
	private static Integer timeAlive = 0;
	private static int optimalDistance = 10;
	private static int heuristic = 0;
	// directions
	public static boolean[] directions = new boolean[4];
	public static int currentDirection = 2;
//	public static boolean down = false;
//	public static boolean left = false;
//	public static boolean right = true;
//	public static boolean pressed = false;
	

	
	@Override
	protected void paintComponent(Graphics g){
		
		// refresh board
		super.paintComponent(g);
		setBackground(Color.BLACK);
		
		// set font
		Font font = new Font("Helvetica", Font.BOLD, 50);
        g.setFont(font);
        FontMetrics metr = getFontMetrics(font);
        
        //set message
        sscore = "SCORE: " + score.toString() + "  MOVE#: " + timeAlive.toString();
        
		if (gameCont){
			// draw border
			g.setColor(Color.GREEN);
			g.drawRect(0,0,B_DIMEN, B_DIMEN);
					
			// draw score			
			g.drawString(sscore,  10, B_DIMEN + font.getSize());
			
			
			// draw apple
			g.setColor(Color.RED);
			g.fillRect(appleX, appleY, BLOCKSIZE, BLOCKSIZE);
			
			// draw snake
			for (int z = 0; z < snakeLen; z++) {
	            if (z == 0) {
	            	g.setColor(Color.GREEN);
	                g.fillRect(x[z], y[z], BLOCKSIZE,BLOCKSIZE);
	            } else {
	            	g.setColor(Color.GRAY);
	                g.fillRect( x[z], y[z], BLOCKSIZE,BLOCKSIZE);
	            }
	        }
			
		}else{
			
			// game over
			String message = "GAME OVER";
			g.setColor(Color.GREEN);
			g.drawString(message, (B_DIMEN - metr.stringWidth(message))/2, W_HEIGHT/2 - font.getSize());
			
			// score
			g.drawString(sscore, (B_DIMEN-metr.stringWidth(sscore)) /2, W_HEIGHT/2 );
			
			
		}
		
		
	}
	
	public Snake(JFrame window){
		//window.addKeyListener(new ArrowAdapter());
		window.setSize(B_DIMEN + 20,W_HEIGHT);  
		
	}
	
	public static void reset(){
		score = 0;
		snakeLen = 3;
		optimalDistance = 10;
		heuristic = 0;
		
		gameCont = true;
		
		timeFromApple = 0;
		timeAlive = 0;
		
		currentDirection = 2;
		
		for(int i = 0; i < 4; i++){
			if(i == currentDirection){
				directions[i] = true;
			}else{
				directions[i] = false;
			}
		}
		makeSnake();
		spawnApple();
	}

	private static void mainLoop(DataOutputStream out, BufferedReader reader, Snake snake)throws InterruptedException, IOException{
		while(gameCont){
			/*
			 if (pause){
			 
				while(pause){
					Thread.sleep(DELAY);
				}
			}
			*/
			System.out.println("what is your move?");
			out.writeUTF("what is your next move?");
			timeFromApple++;
			timeAlive++;
			generateMap(out);
			snake.repaint();
			String direction = reader.readLine();
			switch(Integer.valueOf(direction)){
				case 0:
					System.out.println("we are going to go right");
					directions[currentDirection] = false;
					currentDirection = (currentDirection+3)%4;
					directions[currentDirection] = true;
					break;
				case 1:
					System.out.println("we are going to go straight");
					break;
				case 2:
					System.out.println("we are going to go left");
					directions[currentDirection] = false;
					currentDirection = (currentDirection+1+4)%4;
					directions[currentDirection] = true;
					break;
			}
			/*
			//right = true;
			pressed = true;
			while(!pressed){
				Thread.sleep(DELAY);
			}
						
			//parseData(writer);	
			pressed =false;
  			*/
			Thread.sleep(DELAY);
			//System.out.println("Moving");
			move();
			checkCollisions();	
			if(timeFromApple > 80){
				System.out.println("death by timeOut");
				gameCont = false;
			}
			
		}
		//System.out.println("game over");
		snake.repaint();
		//System.out.println("showing endScreen");
		out.writeUTF(Integer.toString((int) (heuristic + timeAlive/10)));
		//System.out.println("send end result");
		Thread.sleep(200);
	}
	
	public static void startGame(DataOutputStream out, BufferedReader reader) throws InterruptedException, IOException{
		//System.out.println("game started");
		
		// initialize window
		JFrame window = new JFrame();
		window.setTitle("Snake3"); 
		window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		window.setVisible(true);
		window.setFocusable(false);
		window.toBack();
		
		
		
		// initialize game
		
		reset();
		Snake snake = new Snake(window);
		window.add(snake);
		
		//set directions
//		for(int i = 0; i < directions.length; i++){
//			directions[i] = false;
//		}
//		directions[currentDirection] = true;
		while(true){
        	//Thread.sleep(500);
        	out.writeUTF("Do you want to start a game?");
	        System.out.println("asked to start a game");
	        String input = reader.readLine();
	        System.out.println(input);
	        if ( input.contains("yes")){
	        	System.out.print("\n We are going to start the game now \t");
	        	//Snake.gameCont = true;
	        	reset();
	        	mainLoop(out, reader, snake);
	        	
	        	
	        	//out.writeUTF("you lose");
	        }else{
	        	out.writeUTF("goodBye");
	        	break;
	        }
	        
        }
		
		
		
		// display end game
		
		window.dispose();
		System.out.println("window is disposed of");
	}


	private static void generateMap(DataOutputStream out) throws IOException{
		//System.out.println(x[0] +","+ y[0]);
		int[][] map = new int[31][31];
		
		
		int leftwall = 15-x[0]/40;
		int rightwall = 15+(560-x[0])/40;
		int upwall = 15-y[0]/40;
		int downwall = 15+(560-y[0])/40;
		
		
		for(int i = 0; i < 31; i++){
			for(int i2 = 0; i2 < 31; i2++){
				if(i<upwall || i > downwall || i2 < leftwall || i2 > rightwall){
					map[i][i2] = -1;
				}else{
					map[i][i2] = 1;
				}
			}
		}
		
		//adding apple
		map[(appleY - y[0])/40 + 15][(appleX - x[0])/40+15] = 48;
		/*
		map[(appleY - y[0]+40)/40 + 15][(appleX - x[0]+40)/40 + 15] = 10;
		map[(appleY - y[0]+40)/40 + 15][(appleX - x[0]-40)/40 + 15] = 10;
		map[(appleY - y[0]-40)/40 + 15][(appleX - x[0]+40)/40 + 15] = 10;
		map[(appleY - y[0]-40)/40 + 15][(appleX - x[0]-40)/40 + 15] = 10;
		
		map[(appleY - y[0]-40)/40 + 15][(appleX - x[0])/40 + 15] = 10;
		map[(appleY - y[0]+40)/40 + 15][(appleX - x[0])/40 + 15] = 10;
		map[(appleY - y[0])/40 + 15][(appleX - x[0]+40)/40 + 15] = 10;
		map[(appleY - y[0])/40 + 15][(appleX - x[0]-40)/40 + 15] = 10;
		*/

		//adding snake
		for(int i = 1; i < snakeLen; i++){
			int row =  (y[i] - y[0])/40 + 15;
			int col = (x[i] - x[0])/40 + 15;
			map[row][col] = -1;
		}
		
		
		
		map[15][15] = 0;
		//int i = 0;
		//System.out.println("begin sending map");
		if(directions[1]){
			for(int row = 0; row<31; row++){
				for(int col = 0; col<31; col++){
					//System.out.print(i+ ":");
					String message = String.format("%2d", map[row][col]);
					//System.out.println(message);
					out.writeUTF(message);
					//i++;
					
				}
			}
		}else if(directions[0]){
			for(int col = 0; col<31; col++){
				for(int row = 30; row >= 0 ; row--){
					//System.out.print(row+ "," + col + ":");
					String message = String.format("%2d", map[row][col]);
					//System.out.println(message);
					out.writeUTF(message);
					//i++;
					
				}
			}
		}else if(directions[2]){
			for(int col = 30; col >=0; col--){
				for(int row = 0; row<31; row++){
					//System.out.print(i+ ":");
					String message = String.format("%2d", map[row][col]);
					//System.out.println(message);
					out.writeUTF(message);
					//i++;
					
				}
			}
		}else if(directions[3]){
			for(int row = 30; row>= 0; row--){
				for(int col = 30; col >= 0 ; col--){
					//System.out.print(i+ ":");
					String message = String.format("%2d", map[row][col]);
					//System.out.println(message);
					out.writeUTF(message);
					//i++;
					
				}
			}
		}
		
	}
	private static void makeSnake() {
		// TODO Auto-generated method stub
	    for (int z = 0; z < snakeLen; z++) {
	    	x[z] = INITLOCIX - z * BLOCKSIZE;
	        y[z] = INITLOCIY;
	    }
	}
	
	private static void spawnApple(){
		
		int r = (int) (Math.random() * (POSITIONS-2));
        appleX = (r+1) * BLOCKSIZE;

        r = (int) (Math.random() * (POSITIONS-2));
        appleY = (r+1) * BLOCKSIZE;
        
        optimalDistance = Math.abs((x[0] - appleX + y[0] - appleY)/BLOCKSIZE -5); 
	}

	
	private static void move(){
		for (int z = snakeLen; z > 0; z--) {
			
            x[z] = x[(z - 1)];
            y[z] = y[(z - 1)];
        }
		
        if (directions[0]) {
        	//System.out.println("moving to the left");
            x[0] -= BLOCKSIZE;
        }

        if (directions[2]) {
        	//System.out.println("moving to the right");

            x[0] += BLOCKSIZE;
        }

        if (directions[1]) {
        	//System.out.println("moving to the up");

            y[0] -= BLOCKSIZE;
        }

        if (directions[3]) {
        	//System.out.println("moving to the down");

            y[0] += BLOCKSIZE;
        }
	}
	
	private static void checkCollisions(){
		// if snake hits itself
		for (int z = 3; z < snakeLen; z++) {
			if ((x[0] == x[z]) && (y[0] == y[z])) {
				System.out.println("death by itself");
				gameCont = false;
	        }
	    }
		// check if snake hits wall
	    if (y[0] >= B_DIMEN) {
	    	System.out.println("death by wall");
	    	gameCont = false;
	    }

	    if (y[0] < 0) {
	    	System.out.println("death by wall");
	    	gameCont = false;
	    }

	    if (x[0] >= B_DIMEN) {
	    	System.out.println("death by wall");
	    	gameCont = false;
	    }

	    if (x[0] < 0) {
	    	System.out.println("death by wall");
	    	gameCont = false;
	    }
	    // if snake hits apple
	    if ((x[0] == appleX) && (y[0] == appleY)) {
	    	int temp = (int) (snakeLen*100 + 2*(optimalDistance - timeFromApple));
	    	if (temp>4000){
	    		heuristic += 4000;
	    	}else{
	    		heuristic += temp;
	    	}
	    	
	    	timeFromApple = 0;
            snakeLen++;
            score++;
            spawnApple();
        }
	}
	
//	private class ArrowAdapter extends KeyAdapter {
//
//        @Override
//        public void keyPressed(KeyEvent e) {
//
//            int key = e.getKeyCode();
//
//            if ((key == KeyEvent.VK_LEFT) && (!right)) {
//                left = true;
//                up = false;
//                down = false;
//            }
//
//            if ((key == KeyEvent.VK_RIGHT) && (!left)) {
//                right = true;
//                up = false;
//                down = false;
//            }
//
//            if ((key == KeyEvent.VK_UP) && (!down)) {
//                up = true;
//                right = false;
//                left = false;
//            }
//
//            if ((key == KeyEvent.VK_DOWN) && (!up)) {
//                down = true;
//                right = false;
//                left = false;
//            }
//            
//            if (key == KeyEvent.VK_P){
//            	if (pause){
//            		pause = false;
//            	}else{
//            		pause = true;
//            	}
//            }
//            pressed = true;
//        }
//    }

//	@Override
//	public void actionPerformed(ActionEvent e) {
//		// TODO Auto-generated method stub
//		
//	}
}

