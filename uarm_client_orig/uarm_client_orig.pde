
// Need G4P library
import g4p_controls.*;
import processing.serial.*;
import java.text.DecimalFormat;
import java.util.List;
import java.text.SimpleDateFormat;
import java.util.Calendar;

static final  SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

boolean GRAB_EN = false;
boolean SERIAL_EN = false;
boolean YZ_UPDATE = false;
boolean X_UPDATE = false;
boolean GRAB_UPDATE = false;
boolean HAND_UPDATE = false;
boolean LEAP_EN = false;

static String VERSION = "2.0";

static float LIMIT_INIT_X = 0;
static float LIMIT_MIN_X = -300;
static float LIMIT_MAX_X = 300;

static float LIMIT_MIN_Y = 50;
static float LIMIT_MAX_Y = 330;
static float LIMIT_INIT_Y = 150;

static float LIMIT_MIN_Z = -150;
static float LIMIT_MAX_Z = 250;
static float LIMIT_INIT_Z = 100;

static float LIMIT_MIN_HAND = 0;
static float LIMIT_MAX_HAND = 180;
static float LIMIT_INIT_HAND = 90;

String FIRMWARE_VERSION = "N/A";

float current_x = 0;
float current_y = 0;
float current_z = 0;
float current_h = 0;
int limit_leap_min_z = -10;
PrintWriter output;

Serial uPort;

public void settings(){
  size(1024, 500, JAVA2D);
}

public void setup(){
  output = createWriter("logs.txt"); 
  initLeapMotion();
  createGUI();
  customGUI();
  reset();
}

public void draw(){
  background(255);
  if(LEAP_EN)
   leapmotion();
  updatePos();
}

void updatePos(){
  setCurrentPosition();
  if(GRAB_UPDATE){
    setPump();
    GRAB_UPDATE = false;
  }
  if(X_UPDATE){
    setPosition();
    X_UPDATE = false;
  }
  if(HAND_UPDATE){
    setWrist();
    HAND_UPDATE = false;
  }
  if(YZ_UPDATE){
    setPosition();
    YZ_UPDATE = false;
  }  
}

void setCurrentPosition(){
  current_x = slider2d_xy.getValueXF();
  current_z = slider_z_axis.getValueF();
  current_y = slider2d_xy.getValueYF();
  current_h = knob_hand_axis.getValueF();
}

void setUIValue(float x, float y, float z, float h)
{
  slider2d_xy.setValueX(x);
  slider2d_xy.setValueY(y);
  slider_z_axis.setValue(z);
  knob_hand_axis.setValue(h);
}

void initPort(){
  String portName = droplist_serial.getSelectedText();
  printf(portName);
  try{
    uPort = new Serial(this, portName, 115200);
    printf("Connecting to Port:" + portName);
    long startTime = System.currentTimeMillis();
    delay(2000);
    while (false||(System.currentTimeMillis()-startTime)<5000) {
      while (uPort.available() > 0) {
        String line = uPort.readStringUntil('\n');
        println("line:" + line);
        if (line.startsWith("@1")) {
          SERIAL_EN = true;
          button_connect_port.setText("Disconnect");
          break;
        }
      }
      if (SERIAL_EN)
        break;
    }
    if (SERIAL_EN) {
      String msg = "#1 P203\n";
      uPort.write(msg);
      startTime = System.currentTimeMillis();
      while (false||(System.currentTimeMillis()-startTime)<5000) {
        while (uPort.available() > 0) {
          String line = uPort.readStringUntil('\n');
          if (line.startsWith("$1 OK")){
            FIRMWARE_VERSION = line.split(" ")[2];
            label_firmware_vesion_label.setText(FIRMWARE_VERSION);
            break;
          }
        }
        if (FIRMWARE_VERSION != "N/A")
          break;
      }            
      reset();
    }
    else{
      releasePort();
      G4P.showMessage(this, "Firmware Not Correct!", "ERROR", G4P.ERROR);
    }
    
  }catch(Exception e){
    G4P.showMessage(this, "Can't initialize Port" + portName + "Error: " + e, "ERROR", G4P.ERROR);
  }
  
}

void releasePort(){
  try{
     SERIAL_EN = false;
     uPort.stop();
     button_connect_port.setText("Connect");
     label_firmware_vesion_label.setText("N/A");
  }catch(Exception e){
    G4P.showMessage(this, "Can't Disconnect Port", "ERROR", G4P.ERROR);
  }
}

String[] getUArmPorts(){
    List<String> ports = new ArrayList<String>();
  for (String port: Serial.list()) {
    //println('\n' + port + ':');
    String idProduct = Serial.getProperties(port).get("idProduct");
    if ( !port.startsWith("/dev/cu.") && idProduct!= null && idProduct.equals("6001"))
    //if ( !port.startsWith("/dev/cu.") && idProduct!= null )
    {
      ports.add(port);
    }
  }
  String[] stockArr = new String[ports.size()];
  return ports.toArray(stockArr);
}

void reset(){
  setUIValue(LIMIT_INIT_X,LIMIT_INIT_Y,LIMIT_INIT_Z,LIMIT_INIT_HAND);
  button_grab.setText("Catch");
  GRAB_EN = false;
  GRAB_UPDATE = true;
  YZ_UPDATE = true;
  X_UPDATE = true;
  HAND_UPDATE = true;
  GRAB_UPDATE = true;
  updatePos();
}

// Use this method to add additional statements
// to customise the GUI controls
public void customGUI(){
  slider2d_xy.setEasing(5.0);
  droplist_serial.setItems(getUArmPorts(),0);
}

String roundTwoDecimals(float d) {
  DecimalFormat twoDForm = new DecimalFormat("#.#");
  return twoDForm.format(d);
}

void printf(String msg) {
  println(msg);
  msg = sdf.format(Calendar.getInstance().getTime()) + ": " + msg;
  output.println(msg);
  output.flush();
}