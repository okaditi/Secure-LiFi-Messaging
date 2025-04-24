#define LDR_PIN A0
#define SAMPLING_TIME 5

bool previous_state = true;
bool current_state = true;
char buff[64];
bool synced = false; 

void setup() 
{
  Serial.begin(9600);
}

void loop() 
{
  current_state = get_ldr(); 
  if (!current_state && previous_state) 
  {
    char receivedChar = get_byte();
    if (!synced) 
    {
      if (receivedChar == (char)0xFF) 
      {
        synced = true;
      }
    } 
    else 
    {
      if (receivedChar == '\n') 
      {
        synced = false;
        Serial.print("\n");
      } 
      else 
      {
        sprintf(buff, "%c", receivedChar);
        Serial.print(buff);
      }
    }
  }
  previous_state = current_state;
}

bool get_ldr()
{
  bool val = analogRead(LDR_PIN) > 90 ? true : false;
  return val;
}

char get_byte()
{
  char data_byte = 0;
  delay(SAMPLING_TIME * 1.5); 
  for (int i = 0; i < 8; i++) 
  {
    data_byte = data_byte | (char)get_ldr() << i;
    delay(SAMPLING_TIME);
  }
  return data_byte;
}
