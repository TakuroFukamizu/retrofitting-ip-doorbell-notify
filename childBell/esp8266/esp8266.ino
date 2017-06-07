#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>
#include <DFPlayer_Mini_Mp3.h>
#include <PubSubClient.h>

#define MP3_RX 4  // GPIO4
#define MP3_TX 5  // GPIO5

#define TOPIC_CMD "doorbell"
#define CMD_RING "request-ring"

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASS";
const char* mqtt_server = "YOUR_BROKER";
const char* mqtt_user = "YOUR_MQTT_USER";
const char* mqtt_pass = "YOUR_MQTT_USER_PASS";
String clientId;
const int mp3_track_id = 1;

WiFiClient espClient;
PubSubClient client(espClient);
SoftwareSerial mp3Serial(MP3_RX, MP3_TX); // RX, TX

void setup () {
    Serial.begin(9600);
    while (!Serial) {
      ; // wait for serial port to connect. Needed for native USB port only
    }
    mp3Serial.begin(9600);

    // Create a random client ID
    String clientId = "ChildBell-";
    clientId += String(random(0xffff), HEX);

    // setup wifi and mqtt
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
    
    // setup mp3 module(DFPlayer-mini)
    mp3_set_serial(mp3Serial);
    delay(1); // NEED THIS DELAY
    mp3_set_volume(30); // value 0-30
    
    Serial.println("Start");
}
 
void loop() {
    // connect/reconnect to mqtt broker
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
}


// utils

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }
    Serial.println();
    
    String msg((char*)payload);
    if (msg.equalsIgnoreCase(CMD_RING)) {
        mp3_play(mp3_track_id);
        delay(1000);
    }
}

void reconnect() {
    // Loop until we're reconnected
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Attempt to connect
        if (client.connect(clientId.c_str(), mqtt_user, mqtt_pass)) {
            Serial.println("connected");
            // Once connected, publish an announcement...
        //      client.publish("outTopic", "hello world");
            client.subscribe(TOPIC_CMD);
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            // Wait 5 seconds before retrying
            delay(5000);
        }
    }
}
