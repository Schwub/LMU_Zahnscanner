
#include <AccelStepper.h>
#include <ArduinoJson.h>


#define motorInterfaceType 1

#define plainDirPin 24
#define plainStepPin 30

#define rockerDirPin 28
#define rockerStepPin 29
#define rockerLimitSwitch 9 

#define tableDirPin 26
#define tableStepPin 27
#define tableLimitSwitch 8



AccelStepper plainStepper = AccelStepper(motorInterfaceType, plainDirPin, plainStepPin);
AccelStepper rockerStepper = AccelStepper(motorInterfaceType, 11, 24);
AccelStepper tableStepper = AccelStepper(motorInterfaceType, 11, 24);


void setup() {
  plainStepper.setMaxSpeed(500);
  plainStepper.setAcceleration(100);
  pinMode(12, OUTPUT);
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  digitalWrite(12, LOW);
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
    if(operation == "laser" ){
      handleLaser(doc);
    }
    else {
      Serial.println("Invalid Operation: ");
      Serial.println(operation);
    }
  }
}

void handleMove(StaticJsonDocument<512> doc){
  String stepperType = doc["stepper"];
  int distance = doc["distance"];
  AccelStepper stepper = getStepper(stepperType);
  stepper.moveTo(distance);
  while(stepper.currentPosition() != distance) {
    if(stepperType.equals("plainStepper") && digitalRead(rockerLimitSwitch)){
      Serial.println("Limit reached");
      return;
    }
    else if (stepperType.equals("tableStepper") && digitalRead(tableLimitSwitch)){
      Serial.println("Limit reached");
      return;
    }
    stepper.run();
  }
  Serial.println(0);
}

void handleLaser(StaticJsonDocument<512> doc) {
  String laser = doc["laser"];
  bool state = doc["state"];
}

AccelStepper getStepper(String stepper) {
    if(stepper.equals("plainStepper")){
    return plainStepper;
  } else if (stepper.equals("rockerStepper")) {
    return rockerStepper;
  } else if (stepper.equals("tableStepper")) {
    return tableStepper;
  }
}
