import RPi.GPIO


class GPIO(object):

    def __init__(self, addr_pins, en_pin, data_pin):
        self.addr_pins = addr_pins;  # address pins
        self.en_pin = en_pin;  # enable pin
        self.data_pin = data_pin;  # data pin

        RPi.GPIO.setmode(RPi.GPIO.BOARD)
        try:
            # ADR Output setzen
            for pin in self.addr_pins:
                RPi.GPIO.setup(pin, RPi.GPIO.OUT)
                RPi.GPIO.output(pin, RPi.GPIO.LOW)

            RPi.GPIO.setup(self.en_pin, RPi.GPIO.OUT)
            RPi.GPIO.output(self.en_pin, RPi.GPIO.LOW)

            RPi.GPIO.setup(self.data_pin, RPi.GPIO.OUT)
            RPi.GPIO.output(self.data_pin, RPi.GPIO.LOW)
        except KeyboardInterrupt:
            RPi.GPIO.cleanup()

    def enable(self):
        """ Funktion enable: Setzt kurz den Enable Pin und DATA wird in die
            gesetzte Adresse uebernommen."""
        RPi.GPIO.output(self.en_pin, RPi.GPIO.HIGH);
        print "EN is high"
        # time.sleep(0.0001);
        RPi.GPIO.output(self.en_pin, RPi.GPIO.LOW);
        print "EN is low"

    def address(self, a):
        for i in range(0, 6):  # ADR[0]=11, ADR[1]=12...
            RPi.GPIO.output(self.addr_pins[i], ((1 << i) & a))

    def set_addr(self, addr):
        self.address(addr)  # Addresse anlegen"
        RPi.GPIO.output(self.data_pin, 1);  # Data auf 1 fuer Spuelen setzen
        self.enable()  # Data auf Adresse uebenehmen
        print "adr: %d - %d" % (addr, 1)
        
    def reset(self):
        RPi.GPIO.output(self.data_pin,0);     # Spuelvorgang beenden
        self.enable()                 # Data auf Adresse uebenehmen
        print "adr: %d - %d" % (0,0)

    def cleanup(self):
        RPi.GPIO.cleanup()