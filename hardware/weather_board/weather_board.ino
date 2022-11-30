#include <ESP8266WiFi.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

const char* nameWifi = "name";
const char* passWifi = "password";
const char* server = "0.0.0.0";
String data = "";
WiFiClient client;

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

void sendData(String info) {
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
}

void loop() {
  data = Serial.readString();
  if (data != "") {
    data.remove(data.length() - 1, 2);
    Serial.print(data);
    sendData(data);
  }
}