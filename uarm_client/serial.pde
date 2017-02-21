
void setPosition(){
    String msg = "#1 G0 X" + roundTwoDecimals(current_x) + " Y" + roundTwoDecimals(current_y) + " Z" + roundTwoDecimals(current_z) + " F0\n";
  //  printf(msg);
   if(SERIAL_EN)
     uPort.write(msg);  
}

void setPump(){
    int pump_status = 0;
    if (GRAB_EN)
      pump_status = 1;
    else
      pump_status = 0;
    String msg_pump = "#1 M231 V"+ pump_status + "\n";
    String msg_gripper = "#1 M232 V"+ pump_status + "\n";
    printf(msg_pump);
    printf(msg_gripper);
   if(SERIAL_EN){
     uPort.write(msg_pump);
     uPort.write(msg_gripper);
   }
}

void setWrist(){
    String msg = "#1 G202 N3 V" + current_h + "\n";
    printf(msg);
   if(SERIAL_EN)
     uPort.write(msg);    
}

void stop() {
  // Clear the buffer, or available() will still be > 0
  uPort.clear();
  // Close the port
  uPort.stop();
} 