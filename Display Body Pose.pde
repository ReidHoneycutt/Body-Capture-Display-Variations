import java.io.*;
import java.net.*;
import java.util.*;
import java.nio.ByteBuffer;
import processing.sound.*;


Socket socket;
InputStream is;
byte[] buffer = new byte[1024];
Vector<float[]> coords = new Vector<float[]>();

void setup() {
  
  //fullScreen();
  size(900, 900);
  strokeCap(CORNER);
  stroke(255);
  // establish a connection
  try {
      socket = new Socket("127.0.0.1", 5000);
      is = socket.getInputStream();
      System.out.println("Connected");
  }
  catch (UnknownHostException u) {
      System.out.println(u);
      return;
  }
  catch (IOException i) {
      System.out.println(i);
      return;
  }
  //preload_objects();
}
void read_and_parse() {
  int data_len;
  int num_hands;
  int num_landmarks;
  try {
    byte[] len_buffer = new byte[4];
    byte[] num_hand_buffer = new byte[1];
    byte[] num_landmark_buffer = new byte[1];
    
    is.read(len_buffer, 0, 4);
    is.read(num_hand_buffer, 0, 1);
    is.read(num_landmark_buffer, 0, 1);
    
    data_len = ByteBuffer.wrap(len_buffer).getInt();
    num_hands = Byte.toUnsignedInt(num_hand_buffer[0]);
    num_landmarks = Byte.toUnsignedInt(num_landmark_buffer[0]);
    
    // Read in the actual hand data
    byte[] data_buffer = new byte[data_len];
    is.read(data_buffer, 0, data_len);
    
    String data = new String(data_buffer, 0, data_len);
    String[] delimited_coords = data.split("@");
    coords = new Vector<float[]>();
    for (int i = 0; i < num_landmarks -1; i++) {
      String[] p = delimited_coords[i].split(":");
      if (p.length == 2) {
        float[] c = {width - width * float(p[0]), height * float(p[1])};
        coords.add(c);
        //vertex(width - width * float(p[0]), height * float(p[1]));
      }
    }
  } catch (IOException i) {
    System.out.println(i);
  }
} 
float R = 200;
void draw() {
  try {
    if (is.available() > 0) {
      background(0);
      read_and_parse();
      display_body();  
    }
  } catch (IOException i) {
      System.out.println(i);
      return;
  }
}
void display_body() {
  for (int i = 0; i < coords.size(); i++) {
    ellipse(coords.get(i)[0], coords.get(i)[1], 20, 20);
  }
}
