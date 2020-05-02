from m5stack import *
from uiflow import *
from m5ui import *

# Draw the arc with center at (x,y) and radius r, starting at angle start and ending at angle end
# The thicknes of the arc outline is set by the thick argument
# If fillcolor is given, filled arc will be drawn.
#lcd.arc(x, y, r, thick, strat, end [,color, fillcolor])

def display(level):
  lcd.print("moisture", lcd.CENTER, 10)
  lcd.print("level :", lcd.CENTER, 30)
  lcd.print(level, lcd.CENTER, 60)
  
  arc_level = -140 + 280*(level/1000)
  
  lcd.arc(40, 120, 30, 10, -140, 140, 0x6666FF, 0x000000)
  for x in range(-140, arc_level, 3):
    lcd.arc(40, 120, 30, 10, -140, x, 0x0000ff)