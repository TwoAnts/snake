# README #   
多方向版本，把上下左右四个方向，变成了八个方向。


## Something To Say ##  

1.我将 __贪吃蛇__ 本身的游戏逻辑，独立为一个类，只要使用简单方法调用,
就可以驱动这个游戏和获得游戏的状态
  
2.主要使用 __Tkinter.Canvas__ 类

3.写的过程中，为了解决蛇的间歇性前进问题，尝试了许多方法。 
使用 __threading__ 和 __timer__ ，后来用了一下，发现其他的线程会卡住，效果不理想
使用`after()`方法，让timerHandler对自己进行间歇性的调用，总算实现了我要的效果。这里是自己调用自己，但不是递归。方法不会阻塞。

## How To Play ##  
`python snake.py`
 
This game uses `Tkinter` module. It can run on all platforms with python.

