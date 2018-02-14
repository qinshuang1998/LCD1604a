# LCD1604a
树莓派驱动1604液晶屏的封装类

使用说明：

````
import pi1604                      #导入类
lcd = pi1604.LCD1604()             #实例化对象
lcd.lcd_clear()                    #调用lcd_clear方法(初始化液晶屏)
lcd.lcd_string("hello world!",1)   #在屏幕第一行输出hello world!
````