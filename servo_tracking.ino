//Sketch based on work done by Robin2 on the arduino forum
//more info here
//https://forum.arduino.cc/index.php?topic=225329.msg1810764#msg1810764


#include <Servo.h>

Servo panServo;
Servo tiltServo; 

const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

float panServoAngle = 90.0;
float tiltServoAngle = 90.0;

//8=============D

void setup() {
  Serial.begin(115200);
  
  panServo.attach(8);
  tiltServo.attach(9);
  
  //moveServo();
  start_sequence();

  delay(200);
  
  Serial.println("<Hasta la vista baby>"); // send message to computer
}

//8=============D

void loop() {
  getDataFromPC();
  replyToPC();
  moveServo();
}

//8=============D

void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();              //read char from serial
      
    if (x == endMarker) {                //look for end marker
      readInProgress = false;            //if found, set read in progress true (will stop adding new byte to buffer)
      newDataFromPC = true;              //let arduino know that new data is available
      inputBuffer[bytesRecvd] = 0;       //clear input buffer
      processData();                      // process data in buffer
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;      //populate input buffer with bytes
      bytesRecvd ++;                    //increment index
      if (bytesRecvd == buffSize) {     //when buffer is full
        bytesRecvd = buffSize - 1;      //keep space for end marker
      }
    }

    if (x == startMarker) {              // look for start maker
      bytesRecvd = 0;                    // if found, set byte received to 0
      readInProgress = true;             // set read in progress true
    }
  }
}

//8=============D

void processData() // for data type "<float, float, int>" 
{
  char * strtokIndx; // this is used by strtok() as an index

   strtokIndx = strtok(inputBuffer,",");      // get the first part
   panServoAngle = atof(strtokIndx);         // convert this part to a float

   strtokIndx = strtok(NULL,",");          // get the second part(this continues where the previous call left off)
   tiltServoAngle = atof(strtokIndx);     // convert this part to a float

   strtokIndx = strtok(NULL, ",");      // get the last part
  
}

//8=============D

void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<");
    Serial.print(panServo.read());
    Serial.print(",");
    Serial.print(tiltServo.read());
    Serial.println(">");
  }
}

//8=============D

void moveServo() 
{
  panServo.write(panServoAngle);
  tiltServo.write(tiltServoAngle);
}

//8=============D
 void start_sequence()
  {
    panServo.write(90);
    tiltServo.write(90);
    delay(300);
  }
