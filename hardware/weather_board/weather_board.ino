#include <ESP8266WiFi.h>
#include <Wire.h>
//#include <Adafruit_Sensor.h>
//#include <Adafruit_BMP280.h>
#include "WiFiCredentials.h"

const char* nameWifi = NAME;
const char* passWifi = PASSWORD;
const char* server = "0.0.0.0";
String data = "";
WiFiClient client;

struct ResponceData{
  int temperature;
  int humidity;
  int pressure;
  int windSpeed;
  String windDirection;
  int rain;
};

void setup() {

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

void printData(ResponceData data){
  Serial.println(data.temperature);
  Serial.println(data.humidity);
  Serial.println(data.pressure);
  Serial.println(data.windSpeed);
  Serial.println(data.windDirection);
  Serial.println(data.rain);
}

/*void sendData(ResponceData data) {
  if (client.connect(server, 8000)) {
    String message = "{\"message\": \"";
    message += info;
    //message.remove(zprava.length()-1,2);
    message += "\"}";
    Serial.println(message);
    client.println("POST /post_data HTTP/1.1");
    client.print("Host: ");
    client.println(server);
    client.println("Connection: close");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(message.length());
    client.println();
    client.print(message);
  }
  client.stop();
  Serial.println("Data sent");
}*/

int getTemperature(){
  return 1;
}

int getHumidity(){
  return 2;
}

int getPressure(){
  return 3;
}

int getWindSpeed(){
  return 4;
}

String getWindDirection(){
  return "A";
}

int getRain(){
  return 5;
}

void loop() {
  ResponceData data;
  data.temperature = getTemperature();
  data.humidity = getHumidity();
  data.pressure = getPressure();
  data.windSpeed = getWindSpeed();
  data.windDirection = getWindDirection();
  data.rain = getRain();
  printData(data);
  delay(3000);
}