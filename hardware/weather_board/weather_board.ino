#include <ESP8266WiFi.h>
#include <Wire.h>
#include <AS5600.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_AM2320.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>
#include "env.h"

#define BMP280_ADRESS (0x76)
#define RAIN_PIN 12
#define TX 6
#define RX 13

TinyGPSPlus gps;
SoftwareSerial swSerial(RX, TX);
Adafruit_AM2320 am2320 = Adafruit_AM2320();
Adafruit_BMP280 bmp;
AS5600 as5600;
WiFiClientSecure client;
const int WIND_SPEED_PIN = 14;
const int correction = 32;
const char* nameWifi = NAME;
const char* passWifi = PASSWORD;
const char* server = SERVER;
const char* token = TOKEN;
const int VOLUME = 1;

int windSpeedState = 0;
float currentRain = 0;
float distancePerTict = 0.036717364138831;
String GPS = "0.0_0.0";
String data = "";

struct ResponseData {
  float temperature;
  float humidity;
  float pressure;
  float windSpeed;
  String windDirection;
  float rain;
};


void ICACHE_RAM_ATTR rainSwitch() {
  currentRain += VOLUME;
}

void setup() {
  pinMode(RAIN_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(RAIN_PIN), rainSwitch, FALLING);
  pinMode(WIND_SPEED_PIN, INPUT);
  pinMode(2, OUTPUT);
  windSpeedState = digitalRead(WIND_SPEED_PIN);
  as5600.begin(4);
  as5600.setDirection(AS5600_CLOCK_WISE);
  am2320.begin();
  bmp.begin(BMP280_ADRESS);
  swSerial.begin(9600);


  Serial.begin(9600);
  WiFi.begin(nameWifi, passWifi);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to Wifi ");
  Serial.println(nameWifi);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}


String getJSON(ResponseData data) {
  String message = "{\"temperature\":" + (String)data.temperature + ", \"humidity\":" + (String)data.humidity + ", \"pressure\":" + (String)data.pressure;
  message += ", \"wind_speed\":" + (String)data.windSpeed + ", \"wind_direction\": \"" + data.windDirection + "\", \"rain\":" + (String)data.rain + "}";
  return message;
}

void sendData(ResponseData data) {
  client.setInsecure();
  if (client.connect(server, 443)) {
    String message = getJSON(data);
    client.println("POST /api/station/update HTTP/1.1");
    client.print("Host: ");
    client.println(server);
    client.println("Connection: close");
    client.print("Authorization:Bearer ");
    client.println(token);
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(message.length());
    client.println();
    client.print(message);
    Serial.println("Data sent");
    while (client.connected()) {
      Serial.println(client.readStringUntil('\n'));
    }
  } else {
    Serial.println("Connection failed");
  }
  client.stop();
}

void getGPS() {
  while (swSerial.available() > 0) {
    gps.encode(swSerial.read());
    yield();
  }
  if (gps.location.isUpdated()) {
    Serial.print("LAT=");
    Serial.print(gps.location.lat(), 6);
    Serial.print("LNG=");
    Serial.println(gps.location.lng(), 6);
    float lat = gps.location.lat();
    float lng = gps.location.lng();
    GPS = String(lat) + "_" + String(lng);
  }
  Serial.println(GPS);
}

float getTemperature() {
  return am2320.readTemperature();
}

float getHumidity() {
  return am2320.readHumidity();
}

float getPressure() {
  return bmp.readPressure();
}

float getWindSpeed() {
  int tick = 0;
  int state = digitalRead(WIND_SPEED_PIN);
  unsigned long start = millis();
  while ((millis() - start) <= 60000) {
    if (digitalRead(WIND_SPEED_PIN) == 0 && state == 1) {
      tick++;
      state = false;
    } else if (digitalRead(WIND_SPEED_PIN) == 1 && state == 0) {
      tick++;
      state = true;
    }
    yield();
  }
  return tick * distancePerTict / 60;
}

String getWindDirection() {
  int angle = as5600.readAngle();
  if (angle > 256 && angle <= 768) {
    return "NE";
  } else if (angle > 768 && angle <= 1280) {
    return "E";
  } else if (angle > 1280 && angle <= 1792) {
    return "SE";
  } else if (angle > 1792 && angle <= 2304) {
    return "S";
  } else if (angle > 2304 && angle <= 2816) {
    return "SW";
  } else if (angle > 2816 && angle <= 3328) {
    return "W";
  } else if (angle > 3840 || angle <= 256) {
    return "N";
  } else {
    return "NW";
  }
}


float getRain() {
  float x = currentRain / 1000 * 60 / 0.005411;
  currentRain = 0;
  return x;
}

void loop() {
  if (GPS == "0.0_0.0") {
    getGPS();
  } else {
    ResponseData data;
    data.windSpeed = getWindSpeed();
    data.temperature = getTemperature();
    delay(100);
    data.humidity = getHumidity();
    data.pressure = getPressure();
    data.windDirection = getWindDirection();
    data.rain = getRain();
    Serial.println(getJSON(data));
    //sendData(data);

    delay(1000);
  }
}
