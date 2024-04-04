from machine import Pin, I2C, PWM
import ssd1306
import framebuf
from time import sleep_ms
import utime
import _thread as th


losser = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x00\x00\x00\x00\x07\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x03\xfc\x00\x00\x00\x00\x0f\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x07\xfe\x00\x00\x00\x00\x7f\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xe0\x00\x00\x01\xff\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x01\xff\xf0\x00\x00\x01\xff\xf0\x00\x00\x01\xff\xff\xf0\x00\x00\x00\xff\xf8\x00\x00\x00\xff\xfc\x00\x00\x0f\xff\xff\xff\x00\x00\x03\xff\xf0\x00\x00\x00\x3e\x3f\x00\x00\x67\xff\xff\xfc\xe0\x00\x0f\xc7\xc0\x00\x00\x00\x00\x1f\x00\x03\xdf\xff\xff\xff\xbc\x00\x0f\x80\x00\x00\x00\x00\x00\x0f\xc0\x0f\x5f\xff\xff\xff\xaf\x00\x7f\x00\x00\x00\x00\x00\x00\x03\xf0\x1d\xbf\xff\xff\xff\xd3\x80\xfc\x00\x00\x00\x00\x00\x00\x00\xf8\x7f\xff\xff\xff\xff\xff\xe1\xf0\x00\x00\x00\x00\x00\x00\x00\xfc\xff\xff\xff\xff\xff\xff\xf7\xe0\x00\x00\x00\x00\x00\x00\x00\x3c\x00\x00\x00\x00\x00\x00\x07\x80\x00\x00\x00\x00\x00\x00\x00\x1b\xff\xff\xff\xff\xff\xff\xf9\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\xff\xff\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xff\xff\xff\xff\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xf0\x3f\xff\xc1\xff\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x07\xff\xc0\x0f\xff\x00\x3f\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\x80\x07\xfc\x00\x1f\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\x80\x07\xfc\x00\x1f\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x80\x07\xfe\x00\x1f\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xc0\x0f\xff\x00\x3f\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xf8\x7f\xff\xe1\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\xff\x0f\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\xfc\x03\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xf8\x03\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3f\xfc\x07\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x8f\xff\x0f\xff\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x7e\x1f\xff\x87\xec\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x7f\xc0\x00\x3f\xee\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x0f\xdf\x9f\xbf\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3f\xff\x3f\x9f\xcf\xff\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7d\xff\x00\x00\x0f\xf3\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x01\xf8\xe6\xff\x9f\xf6\xf1\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x07\xe1\xfc\xff\x9f\xf3\xf8\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x81\xff\xe0\x00\x7f\xf8\x1f\x00\x00\x00\x00\x00\x00\x00\x1f\x1f\x80\xff\xff\xff\xff\xf0\x1f\x8f\x80\x00\x00\x00\x00\x00\xff\xfe\x00\x7f\xff\xff\xff\xe0\x07\xff\xe0\x00\x00\x00\x00\x00\xff\xf8\x00\x7f\xff\xff\xff\xe0\x01\xff\xf0\x00\x00\x00\x00\x00\xff\xfc\x00\x1f\xff\xff\xff\x80\x07\xff\xe0\x00\x00\x00\x00\x00\x3f\xff\x00\x07\xff\xff\xfe\x00\x0f\xff\xc0\x00\x00\x00\x00\x00\x07\xff\x00\x01\xff\xff\xf8\x00\x0f\xfc\x00\x00\x00\x00\x00\x00\x03\xfe\x00\x00\x0f\xff\x00\x00\x07\xfc\x00\x00\x00\x00\x00\x00\x00\xf8\x00\x00\x00\x00\x00\x00\x01\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')


i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
display = ssd1306.SSD1306_I2C(128, 64, i2c)  # display object


button = Pin(4, Pin.IN, Pin.PULL_UP)
buzzer_pin = Pin(23, Pin.OUT)
buzzer_pwm = PWM(buzzer_pin)


Player_Position = 120
upper_line_limit_1 = 20
lower_line_limit_1 = 42

upper_line_limit_2 = 24
lower_line_limit_2 = 42

upper_line_limit_3= 20
lower_line_limit_3 = 38

upper_line_limit_4 = 30
lower_line_limit_4 = 45

upper_line_limit_5 = 26
lower_line_limit_5 = 40

upper_line_limit_6 = 22
lower_line_limit_6 = 38

upper_line_limit_7 = 24
lower_line_limit_7 = 40

line_limit_1 = 0
line_limit_2 = 0
line_limit_3 = 0
line_limit_4 = 0
line_limit_5 = 0
line_limit_6 = 0
line_limit_7 = 0


stop= 0

start_time = 0


def get_ms():
    return utime.ticks_ms()


def buzz(duration_ms, frequency):
    buzzer_pwm.freq(frequency)  # Set the PWM frequency
    buzzer_pwm.duty(512)        # Set the PWM duty cycle (50% for a beep)
    sleep_ms(duration_ms)
    buzzer_pwm.duty(0)

buzz(500, 880)
sleep_ms(1000)

game_over_song = [
    (330, 200), (294, 200), (262, 400)
]

win_song = [
    (330, 200),  # E
    (392, 200),  # G
    (440, 200),  # A
    (494, 400)   # B
]

def win(score):
        display.fill(0)
        display.text('You Win!', 20, 27, 1)
        display.text('Time:{}'.format(score), 20, 40, 1)
        display.show()
        for duration, freq in game_over_song:
            buzz(duration, freq)

def collision():
        fb = framebuf.FrameBuffer(losser, 128, 64, framebuf.MONO_HLSB)
        display.fill(0)
        display.blit(fb, 8, 0)
        display.text('Game', 0, 27, 1)
        display.text('Over', 0, 40, 1)
        display.show()
        for duration, freq in game_over_song:
            buzz(duration, freq)
        

    
def count_score():
    current_time = get_ms()
    elapsed_time = current_time - start_time
    score = int(elapsed_time/100)
    return score
    

start_time = get_ms()

while stop == 0:
    
    # We are using 2 color screen. 0 is black. 1 is white
    # clear the screen:
    
    display.fill(0)
      
    
    score = count_score()

    #Left Cage
    display.hline(0, 22, 10, 1)
    display.hline(0, 44, 10, 1)
    display.vline(10, 22, 4, 1)
    display.vline(10, 40, 4, 1)
    display.text('B', 2, 8, 1)

    #Right Cage
    display.hline(117, 22, 10, 1)
    display.hline(117, 44, 10, 1)
    display.vline(117, 22, 4, 1)
    display.vline(117, 40, 4, 1)
    display.text('A', 118, 8, 1)

    #The player
    display.fill_rect(Player_Position, 30, 5, 5, 1)
    
    display.text('T:{}'.format(score), 45, 57, 1)

    #Dircetion Text
    #display.text(dirl, 100, 57, 1)

    if line_limit_1 == 0 and upper_line_limit_1 < 40 :
         upper_line_limit_1 += 2
         lower_line_limit_1 += 2
    else:
        line_limit_1 = 1
        upper_line_limit_1 -= 1
        lower_line_limit_1 -= 1
        if upper_line_limit_1 < 20:
            line_limit_1 = 0
            
    if line_limit_2 == 0 and upper_line_limit_2 < 40 :
         upper_line_limit_2 += 2
         lower_line_limit_2 += 2
    else:
        line_limit_2 = 1
        upper_line_limit_2 -= 1
        lower_line_limit_2 -= 1
        if upper_line_limit_2 < 20:
            line_limit_2 = 0
            
    if line_limit_3 == 0 and upper_line_limit_3 < 40 :
         upper_line_limit_3 += 1
         lower_line_limit_3 += 1
    else:
        line_limit_3 = 1
        upper_line_limit_3 -= 2
        lower_line_limit_3 -= 2 
        if upper_line_limit_3 < 20:
            line_limit_3 = 0
    #---------------------3----------
    if line_limit_4 == 0 and upper_line_limit_4 < 40 :
         upper_line_limit_4 += 1
         lower_line_limit_4 += 1
    else:
        line_limit_4 = 1
        upper_line_limit_4 -= 1
        lower_line_limit_4 -= 1
        if upper_line_limit_4 < 20:
            line_limit_4 = 0
            
    if line_limit_5 == 0 and upper_line_limit_5 < 40 :
         upper_line_limit_5 += 1
         lower_line_limit_5 += 1
    else:
        line_limit_5 = 1
        upper_line_limit_5 -= 1
        lower_line_limit_5 -= 1
        if upper_line_limit_5 < 20:
            line_limit_5 = 0
            
    if line_limit_6 == 0 and upper_line_limit_6 < 40 :
         upper_line_limit_6 += 1
         lower_line_limit_6 += 1
    else:
        line_limit_6 = 1
        upper_line_limit_6 -= 1
        lower_line_limit_6 -= 1
        if upper_line_limit_6 < 20:
            line_limit_6 = 0
            
    if line_limit_7 == 0 and upper_line_limit_7 < 40 :
         upper_line_limit_7 += 1
         lower_line_limit_7 += 1
    else:
        line_limit_7 = 1
        upper_line_limit_7 -= 1
        lower_line_limit_7 -= 1
        if upper_line_limit_7 < 20:
            line_limit_7 = 0
#----------------------------
            
    display.vline(20, 0, upper_line_limit_1, 1)
    display.vline(20, lower_line_limit_1, 14, 1)
    
    display.vline(35, 0, upper_line_limit_2, 1)
    display.vline(35, lower_line_limit_2, 14, 1)
    
    display.vline(50, 0, upper_line_limit_3, 1)
    display.vline(50, lower_line_limit_3, 14, 1)
    
    display.vline(65, 0, upper_line_limit_4, 1)
    display.vline(65, lower_line_limit_4, 14, 1)
    
    display.vline(80, 0, upper_line_limit_5, 1)
    display.vline(80, lower_line_limit_5, 14, 1)
    
    display.vline(95, 0, upper_line_limit_6, 1)
    display.vline(95, lower_line_limit_6, 14, 1)
    
    display.vline(112, 0, upper_line_limit_7, 1)
    display.vline(112, lower_line_limit_7, 14, 1)
    
    
    
    #display.vline(104, 0, 24, 1)
    #display.vline(104, 40, 14, 1)

    button_pressed = not button.value()
    # calculate new position:
    if button_pressed: # button is pressed
        if Player_Position > 5:
            Player_Position -= 1
            #th.start_new_thread(buzz,(50, 880))
            #th.start_new_thread(buzz,(50, 880))
            #buzz(10,880)

        else:
            stop = 1
            win(score)
            sleep_ms(5000)
            Player_Position = 120
            start_time = get_ms()
            stop = 0

    display.show()
    
      
    if Player_Position <= 20 and 20 <= (Player_Position + 5):
        if upper_line_limit_1 >= 30 or lower_line_limit_1 <= 35:
            stop = 1
            collision()
            sleep_ms(3000)
            Player_Position = 120
            start_time = get_ms()
            stop = 0
            
    elif Player_Position <= 35 and 35 <= (Player_Position + 5):
        if upper_line_limit_2 >= 30 or lower_line_limit_2 <= 35:
            stop = 1
            collision()
            sleep_ms(3000)
            Player_Position = 120
            start_time = get_ms()
            stop = 0
            
    elif Player_Position <= 50 and 50 <= (Player_Position + 5):
        if upper_line_limit_3 >= 30 or lower_line_limit_3 <= 35:
            stop = 1
            collision()
            sleep_ms(3000)
            Player_Position = 120
            start_time = get_ms()
            stop = 0
        
    elif Player_Position <= 65 and 65 <= (Player_Position + 5):
        if upper_line_limit_4 >= 30 or lower_line_limit_4 <= 35:
            stop = 1
            collision()
            sleep_ms(3000)
            Player_Position = 120
            start_time = get_ms()
            stop = 0
            
            
    elif Player_Position <= 80 and 80 <= (Player_Position + 5):
        if upper_line_limit_5 >= 30 or lower_line_limit_5 <= 35:
            stop = 1
            collision()
            sleep_ms(3000)
            Player_Position = 120
            start_time = get_ms()
            stop = 0
            
    elif Player_Position <= 95 and 95 <= (Player_Position + 5):
        if upper_line_limit_6 >= 30 or lower_line_limit_6 <= 35:
            stop = 1
            collision()
            sleep_ms(3000)
            Player_Position = 120
            start_time = get_ms()
            stop = 0
            
    elif Player_Position <= 112 and 112 <= (Player_Position + 5):
        if upper_line_limit_7 >= 30 or lower_line_limit_7 <= 35:
            stop = 1
            collision()
            sleep_ms(3000)
            Player_Position = 120
            start_time = get_ms()
            stop = 0
            

        
# our screen:
# 0,0			127,0
#
# 0,63			127,63
