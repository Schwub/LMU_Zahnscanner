#define plainDirPin 7
#define plainStepPin 13

#define rockerDirPin 6
#define rockerStepPin 12
#define rockerLimitSwitch 4 

#define tableDirPin 5
#define tableStepPin 11
#define tableLimitSwitch 3

#define right HIGH
#define left LOW

#define rightLaser 10
#define leftLaser 9

//Test
#define delayTime 1000
//Production
//#define delayTime 1000


void setup() {
  //Setup Laser
  pinMode(rightLaser, OUTPUT);
  pinMode(leftLaser, OUTPUT);

  //Setup Plain Stepper
  pinMode(plainStepPin, OUTPUT);
  pinMode(plainDirPin, OUTPUT);

  //Setup Rocker Stepper
  pinMode(rockerStepPin, OUTPUT);
  pinMode(rockerDirPin, OUTPUT);

  //Setup Table Stepper
  pinMode(tableStepPin, OUTPUT);
  pinMode(tableDirPin, OUTPUT);

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
  int tableLimitSwitchState;
  int rockerLimitSwitchState;
  
  //
  while(Serial.available() > 0) {
    String serialData = Serial.readStringUntil('\n');

      tableLimitSwitchState = digitalRead(tableLimitSwitch);
      rockerLimitSwitchState = digitalRead(rockerLimitSwitch);

      if(rockerLimitSwitchState == LOW) {
        Serial.println("ES10");
      }
      else if(rockerLimitSwitchState == HIGH) {
        Serial.println("ES11");
      }
      
      if(tableLimitSwitchState == LOW) {
        Serial.println("ES20");
      }
      else if(tableLimitSwitchState == HIGH) {
        Serial.println("ES21");
      }

      Serial.println(serialData);
      if(serialData[0] == 'L' ){
        handleLaser(serialData);
      }
      else if (serialData.equals("S10")) {
        digitalWrite(plainDirPin, HIGH);
        oneStep(plainStepPin);
      }
      else if (serialData.equals("S11")) {
        digitalWrite(plainDirPin, LOW);
        oneStep(plainStepPin);
      }
      else if (serialData.equals("S20")) {
        digitalWrite(rockerDirPin, HIGH);
        oneStep(rockerStepPin);
      }
      else if (serialData.equals("S21")) {
        digitalWrite(rockerDirPin, LOW);
        oneStep(rockerStepPin);
      }
      else if (serialData.equals("S30")) {
        digitalWrite(tableDirPin, HIGH);
        oneStep(tableStepPin);
      }
      else if (serialData.equals("S31")) {
        digitalWrite(tableDirPin, LOW);
        oneStep(tableStepPin);
     }
     Serial.println("0");
  }
}

void handleLaser(String serialData){
      if(serialData.equals("L11")){
        digitalWrite(rightLaser, HIGH);
      }
      else if (serialData.equals("L10")) {
        digitalWrite(rightLaser, LOW);
      }
      else if (serialData.equals("L21")) {
        digitalWrite(leftLaser, HIGH);
      }
      else if (serialData.equals("L20")) {
        digitalWrite(leftLaser, LOW);
      }
}

void oneStep(int stepper) {
  digitalWrite(stepper, HIGH);
  delay(delayTime);
  digitalWrite(stepper, LOW);
  delay(delayTime);
}
