#include <Ezo_i2c.h> //include the EZO I2C library from https://github.com/Atlas-Scientific/Ezo_I2c_lib
#include <Wire.h>    //include arduinos i2c library
#include <sequencer2.h> //imports a 2 function sequencer 
#include <Ezo_i2c_util.h> //brings in common print statements
// Note: this file was received as it is from previous developer, but was never test in the last huillin
// so might be needed to do some adjustment to make it work

Ezo_board PH = Ezo_board(99, "PH");       //create a PH circuit object, who's address is 99 and name is "PH"
Ezo_board EC = Ezo_board(100, "EC");      //create an EC circuit object who's address is 100 and name is "EC"
Ezo_board RTD = Ezo_board(102, "RTD");    //create an RTD circuit object who's address is 102 and name is "RTD"

void step1();  //forward declarations of functions to use them in the sequencer before defining them
void step2();

Sequencer2 Seq(&step1, 1000, &step2, 0);  //calls the steps in sequence with time in between them

void setup() {
  Wire.begin();                           //start the I2C
  Serial.begin(9600);                     //start the serial communication to the computer
  Seq.reset();                            //initialize the sequencer
}

void loop() {
  Seq.run();                              //run the sequncer to do the polling
}

void step1(){
   //send a read command. we use this command instead of PH.send_cmd("R"); 
  //to let the library know to parse the reading
  PH.send_read_cmd();                      
  EC.send_read_cmd();
  RTD.send_read_cmd();
}

void step2(){
  receive_and_print_reading(PH);             //get the reading from the PH circuit
  Serial.print(";");
  receive_and_print_reading(EC);             //get the reading from the EC circuit
  Serial.print(";");
  receive_and_print_reading(RTD);             //get the reading from the RTD circuit
  Serial.println();
}
