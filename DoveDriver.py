import machine
import time
from ev3lego_l298 import ev3lego_l298


pir_pin = 13
encoder1_pin=12
encoder2_pin=14
in1_pin=4
in2_pin=6
ena_pin=5
wheel_size=65

class DoveDriver:
   
    
    
    def __init__(self):
   
        self.motion_detected = False

        # Create an instance of the PIRSensor class on GPIO pin 4
        self.pir= machine.Pin(pir_pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        
        # Attach the hardware interrupt handler to detect the rising edge (motion start)
        self.pir.irq(trigger=machine.Pin.IRQ_RISING, handler=self._motion_callback)
        print(f"PIR Sensor initialized on GPIO {pir_pin}.")
        
        
        self.sill_length = 1 # 1 metre of length
        self.motor = ev3lego_l298(encoder1_pin,encoder2_pin,in1_pin,in2_pin,ena_pin,wheel_size)

        print("System armed. Waiting for motion...")
        # Keep the main thread alive; the class handles detection automatically via interrupts
        
                
    def run(self):
       
        # Keep the main thread alive; the class handles detection automatically via interrupts
        while True:
            if self.motion_detected == True:
                """Internal callback function triggered by the hardware interrupt."""
                print("Pigeon detected")
                self.motor.godegreesp(180, 1000, 50, 2, 2) #required angle, number of iterations
                print("Reversing direction")
                time.sleep(5)
                self.motor.brake()
                time.sleep(2)
                self.motor.godegreesp(-180, 1000, 50, 2, 2) #required angle, number of iterations
                time.sleep(5)
                self.motor.brake()
                time.sleep(2)
                self.motion_detected = False

    def _motion_callback(self, pin):
      
        self.motion_detected = True
        
        
