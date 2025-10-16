#include <ESP32Servo.h>
#include <RF24.h>
#include <nRF24L01.h>
#include <SPI.h>

// RADIO
#define CE 22
#define CSN 21
RF24 radio(CE,CSN);
const  uint64_t address = 0xE8E8F0F0E1LL;

struct sendPacket {
  byte lElevon;
  byte rElevon;
  byte throttle;
};

sendPacket controlInputs;

// JOYSTICK
#define JOYSTICK_X 26 // Roll control
#define JOYSTICK_Y 27 // Pitch control
#define JOYSTICK_THROTTLE 32 // ESC Throttle

// Calibration offsets (adjust if needed)
#define LEFT_FLAP_NEUTRAL 90 // Adjust to make left flap perfectly straight
#define RIGHT_FLAP_NEUTRAL 90 // Adjust to make right flap perfectly straight

// ESC Speed
#define MAX_SPEED 1200
#define MIN_SPEED 1000

void setup() {
  Serial.begin(115200);

  radio.begin();
  radio.setChannel(5);
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_HIGH);
  radio.openWritingPipe(address);
  radio.stopListening();
}

void loop() {

  // Read joystick analog values
  int xValue = analogRead(JOYSTICK_X);
  int yValue = analogRead(JOYSTICK_Y);
  int throttle = analogRead(JOYSTICK_THROTTLE);

  Serial.print("x = ");
  Serial.print(xValue); 
  Serial.print(", y = ");
  Serial.print(yValue);
  Serial.print(", throttle raw = ");
  Serial.println(analogRead(JOYSTICK_THROTTLE));


  // Map joystick values (assuming 0-4095 range on ESP32)
  int pitchMovement = map(yValue, 0, 4095, 180, 0); // Inverted mapping for proper motion
  int rollMovement = map(xValue, 0, 4095, 0, 180);
  int throttleMap = constrain(map(analogRead(JOYSTICK_THROTTLE), 2500, 0, MIN_SPEED, MAX_SPEED), MIN_SPEED, MAX_SPEED);

  // Compute final flap positions (adjust around neutral)
  controlInputs.lElevon = constrain(LEFT_FLAP_NEUTRAL + (pitchMovement - 90) + (90 - rollMovement), 0, 180);
  controlInputs.rElevon = constrain(RIGHT_FLAP_NEUTRAL + (pitchMovement - 90) + (rollMovement - 90), 0, 180);

  controlInputs.throttle = map(throttleMap, MIN_SPEED, MAX_SPEED, 0, 255); // limited to 1 byte - remap on uav

  Serial.print("lElevon = ");
  Serial.print(controlInputs.lElevon);
  Serial.print("rElevon = ");
  Serial.print(controlInputs.rElevon);
  Serial.print("throttle = ");
  Serial.print(controlInputs.throttle);

  // Transmit Control Inputs
  Serial.println("sending message...");
  radio.write(&controlInputs, sizeof(sendPacket));

  delay(50); // Small delay for stability
}