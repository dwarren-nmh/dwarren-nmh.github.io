from m5stack import *
from m5ui import *
from uiflow import *
from machine import *
from apps import test
import network, urequests, esp32, wifiCfg, i2c_bus, ustruct, gc
gc.enable()

led = machine.PWM(machine.Pin(10),5000,99)
esp32.wake_on_ext0(pin = machine.Pin(39, mode = Pin.IN), level = esp32.WAKEUP_ALL_LOW)
lcd.setTextColor(0xaaaaaa, lcd.BLACK)
lcd.font(lcd.FONT_Ubuntu)

def get_moisture():
  i2c = i2c_bus.easyI2C(i2c_bus.PORTA, 0x36)
  i2c.write_u8(0x0f, 0x10)
  wait_ms(5)
  val = i2c.read(2)
  val = ustruct.unpack(">H", val)[0]
  return int(val)

while(True):
  axp.setLDO2Volt(3.3) #turn the screen back on
  while not wifiCfg.doConnect('guest', '12345678', lcdShow=True): pass
  wait(1)
  lcd.clear()

  test.display(get_moisture())

  moisture = get_moisture() #get moisture
  try:
    response = urequests.request(
      method='POST',
      url='http://io.adafruit.com/api/v2/dwarrenku/feeds/moisture/data',
      json={'value':moisture},
      headers={'Content-Type':'application/json','X-AIO-Key':'aio_RBra35LUtbXS5JrNDYtSjdkBaKTO'}
    )
    if response.status_code == 200:
      led.duty(99)
      lcd.clear()
      lcd.print("sent", lcd.CENTER, 5)
      lcd.image(0, 50, 'img/success.jpg')
    else:
      lcd.print("request \r\n error", lcd.CENTER, 0, 0xFFFFFF)
      lcd.image(0, 50, 'img/error.jpg')
      led.duty(50)
      wait(10)
    response.close()
  except Exception as e:
    lcd.print("OS error", lcd.CENTER, 0, 0xFFFFFF)
    lcd.image(0, 50, 'img/error.jpg')
    print(e)

  wifiCfg.wlan_sta.active(False)
  wait(2)
  axp.setLDO2Volt(0)
  #lightsleep(60*1000) # one minute
  lightsleep(1800000) #30 minutes