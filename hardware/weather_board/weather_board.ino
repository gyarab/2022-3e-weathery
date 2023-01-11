#include <ESP8266WiFi.h>
#include <Wire.h>
//#include <Adafruit_Sensor.h>
//#include <Adafruit_BMP280.h>
#include "WiFiCredentials.h"

const char* nameWifi = NAME;
const char* passWifi = PASSWORD;
const char* server = SERVER;
const char* token = TOKEN;
String data = "";
WiFiClientSecure client;
int i = 0;

struct ResponseData{
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

void printData(ResponseData data){
  Serial.println(data.temperature);
  Serial.println(data.humidity);
  Serial.println(data.pressure);
  Serial.println(data.windSpeed);
  Serial.println(data.windDirection);
  Serial.println(data.rain);
  Serial.println();
}

String getJSON(ResponseData data){
  String message = "{\"temperature\":"+(String)data.temperature+", \"humidity\":"+(String)data.humidity+", \"pressure\":"+(String)data.pressure;
  message += ", \"wind_speed\":"+(String)data.windSpeed+", \"wind_direction\": \""+data.windDirection+"\", \"rain\":"+(String)data.rain+"}";
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
  }
  client.stop();
}

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
  ResponseData data;
  data.temperature = getTemperature();
  data.humidity = getHumidity();
  data.pressure = getPressure();
  data.windSpeed = getWindSpeed();
  data.windDirection = getWindDirection();
  data.rain = getRain();
  if (i < 2){
    sendData(data);
    i++;
  }
  delay(3000);
}