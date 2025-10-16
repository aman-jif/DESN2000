#include <ESP32Servo.h>
#include <SPI.h>
#include <RF24.h>
#include <nRF24L01.h>

// OLD: 22, 21
// Radio values:
#define CE 22
#define CSN 21
RF24 radio(CE,CSN);
const  uint64_t address = 0xE8E8F0F0E1LL;

struct recievePacket {
  byte lElevon;
  byte rElevon;
  byte throttle;
};
recievePacket controlInputs;

// Elevon Servos
#define SERVO_LEFT_FLAP 32 // Left flap
#define SERVO_RIGHT_FLAP 33 // Right flap
#define ELEVON_NEUTRAL 90
Servo leftFlap;
Servo rightFlap;

// ESC:
#define ESC_PIN 25
#define MAX_SPEED 1200
#define MIN_SPEED 1000
Servo ESC; // intialise ESC object

void setup() {

  delay(1000);
  Serial.println("Starting UAV...");
  Serial.begin(115200) ;

  // Attach Radio
  radio.begin();
  radio.setChannel(5);
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.openReadingPipe(0, address);
  radio.startListening();

  // Attach servos to pins
  leftFlap.attach(SERVO_LEFT_FLAP);
  rightFlap.attach(SERVO_RIGHT_FLAP);

  // Set initial position (neutral position)
  leftFlap.write(ELEVON_NEUTRAL);
  rightFlap.write(ELEVON_NEUTRAL);

  // Attach ESC:
  ESC.attach(ESC_PIN);
}

void loop() {

  // Listen for controller input
  if (radio.available()) {
    Serial.print(millis());
    Serial.print("-> Message Recieved:...");
    radio.read(&controlInputs, sizeof(recievePacket));

    // Debug output
    Serial.print("Left Flap: "); Serial.print(controlInputs.lElevon);
    Serial.print(" | Right Flap: "); Serial.print(controlInputs.rElevon);
  }



  // Move servos
  leftFlap.write(controlInputs.lElevon);
  rightFlap.write(controlInputs.rElevon);

  // // Throttle ESC
  // remap throttle:
  int remappedThrottle = map(controlInputs.throttle, 0, 255, MIN_SPEED, MAX_SPEED);
  Serial.print(" | Throttle: "); 
  Serial.println(remappedThrottle);
  ESC.writeMicroseconds(remappedThrottle);  

  delay(50); // Small delay for stability
}