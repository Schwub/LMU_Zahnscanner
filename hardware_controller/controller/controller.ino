Q
#include <ArduinoJson.h>

#define plainDirPin 7
#define plainStepPin 13

#define rockerDirPin 28
#define rockerStepPin 29
#define rockerLimitSwitch 4 

#define tableDirPin 26
#define tableStepPin 27
#define tableLimitSwitch 3

#define right HIGH
#define left LOW





#define rightLaser 10
#define leftLaser 9


void setup() {
  //Setup Laser
  pinMode(rightLaser, OUTPUT);
  pinMode(leftLaser, OUTPUT);

  //Setup Plain Stepper
  pinMode(plainStepPin, OUTPUT);
  pinMode(plainDirPin, OUTPUT);

  //Setup Limit Switch
  pinMode(rockerLimitSwitch, INPUT);
  pinMode(tableLimitSwitch, INPUT);

  
  //digitalWrite(12, LOW);
  Serial.begin(9600);
}

void loop() {
  handleSerial();
}

void handleSerial() {
  //
  while(Serial.available() > 0) {
    String serialData = Serial.readStringUntil('\n');
    StaticJsonDocument<512> doc;
    DeserializationError error = deserializeJson(doc, serialData);

    if(error) {
      Serial.println(error.c_str());
    }

    String operation = doc["operation"];
    Serial.println("Received Operation: " + operation);
   

    if(operation == "move" ){
      handleMove(doc);
    }
    else if(operation == "laser" ){
      handleLaser(doc);
    }
    else {
      Serial.println("Invalid Operation: ");
      Serial.println(operation);
    }
  }
}

void handleMove(StaticJsonDocument<512> doc) {
  String stepper = doc["stepper"];
  String dir = doc["direction"];
  int steps = doc["steps"];
  Serial.println(dir);
  if( dir.equals("right")){
    digitalWrite(plainDirPin, HIGH);
  } else {
    digitalWrite(plainDirPin, LOW);
  }
  for (int i = 0; i < steps; i++) {
    if(digitalRead(tableLimitSwitch) == LOW) {
      break;
    }
    // These four lines result in 1 step:
    digitalWrite(plainStepPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(plainStepPin, LOW);
    delayMicroseconds(1000);
  }
}

void handleLaser(StaticJsonDocument<512> doc) {
  String laser = doc["laser"];
  String state = doc["state"];
  if(laser.equals("right")){
    if(state.equals("on")){
      digitalWrite(rightLaser, HIGH);
    } else if(state.equals("off")){
      digitalWrite(rightLaser, LOW);
    }
  } else if(laser.equals("left")){
    if(state.equals("on")){
      digitalWrite(leftLaser, HIGH);
    } else if(state.equals("off")){
      digitalWrite(leftLaser, LOW);
    }
  }
}
