#define LED_PIN 9
#define PERIOD 5

char string[64];
int string_length = 0;
bool new_message_received = false;  

void setup() 
{
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Enter the message to send:");
  get_message();
}

void loop() 
{
  if (Serial.available()) {
    get_message();
  }
  send_byte(0xFF);
  for (int i = 0; i <= string_length; i++) {
    send_byte(string[i]);
  }
  delay(1000);  
}

void get_message()
{
  delay(50);  
  do {
    string_length = Serial.readBytesUntil('\n', string, sizeof(string) - 2);
  } while(string_length <= 0);
  string[string_length] = '\n';  
  string[string_length + 1] = '\0';
  Serial.print("Message updated: ");
  Serial.println(string);
  new_message_received = true;  
}

void send_byte(char my_byte)
{
  digitalWrite(LED_PIN, LOW);  
  delay(PERIOD);
  for (int i = 0; i < 8; i++) {
    digitalWrite(LED_PIN, (my_byte & (0x01 << i)) != 0);
    delay(PERIOD);
  }
  digitalWrite(LED_PIN, HIGH);  
  delay(PERIOD);
}
