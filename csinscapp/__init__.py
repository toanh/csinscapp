name = "csinscapp"
version = "0.1.4"

CLICK = 0
MOUSE_DOWN = 1  
MOUSE_MOVE = 2
MOUSE_OVER = 3
MOUSE_OUT  = 4

# tested on remi version = "2020.3.10"
import remi.gui as gui
from remi import start, App
from threading import *
import base64

class Event:
  def __init__(self, type, source, *args):
    self.type = type
    self.control = source
    self.args = args

class Command:
  def __init__(self, command, arg):
    self.command = command
    self.arg = arg

class ControlCommand (Command):
  def __init__(self, command, control, arg):
    self.control = control
    super(ControlCommand, self).__init__(command, arg)

class StyleCommand(ControlCommand):
  def __init__(self, command, control, arg):
    super(StyleCommand, self).__init__(command, control, arg)
  def execute(self):
    self.control.widget.style[self.command] = self.arg

class FunctionCallCommand(ControlCommand):
  def __init__(self, command, control, arg):
    super(FunctionCallCommand, self).__init__(command, control, arg)
  def execute(self):
    self.command(self.arg)

class Color:
  def __init__(self, r = 255, g = 255, b = 255, a = 1.0, parent = None):
    self._r = r
    self._g = g
    self._b = b
    self._a = a
    self.parent = parent

  @property
  def r(self):
    return self._r
  @r.setter
  def r(self, value):
    self._r = value
    self._trigger()

  @property
  def g(self):
    return self._g
  @g.setter
  def g(self, value):
    self._g = value
    self._trigger()

  @property
  def b(self):
    return self._b
  @b.setter
  def b(self, value):
    self._b = value
    self._trigger()

  @property
  def a(self):
    return self._a
  @a.setter
  def a(self, value):
    self._a = value
    self._trigger()


  def _trigger(self):
    if self.parent is not None:
      self.parent(self)

class Control:
  def __init__(self, x, y, width, height):
    self.widget.style["position"] = "absolute;"
    self.widget.style["top"] = f"{y}px;"
    self.widget.style["left"] = f"{x}px;"    
    self.widget.style["white-space"] = "pre-wrap;"
    self._visible = True
    self._bgcolor = Color(0, 0, 0, 1, self._setbgcolor)
    self._color = Color(255, 255, 255, 1, self._setcolor)
    self._padding = [0, 0, 0, 0]
    self._margin = [0, 0, 0, 0]
    self._data = ""
    self._x = x
    self._y = y
    self._width = width
    self._height = height

  @property
  def x(self): 
    return self._x
  @x.setter
  def x(self, value): 
    self._x = value
    if CSinSCApp.buffered_mode:
      CSinSCApp.styles[self]["left"] = f"{self._x}px;"
    else:
      self.widget.style["left"] = f"{self._x}px;"

  @property
  def y(self): 
    return self._y
  @y.setter
  def y(self, value): 
    self._y = value
    if CSinSCApp.buffered_mode:
      CSinSCApp.styles[self]["top"] = f"{self._y}px;"
    else:
      self.widget.style["top"] = f"{self._y}px;"      

  @property
  def width(self): 
    return self._width
  @width.setter
  def width(self, value): 
    self._width = value

    width = self._width
    if not isinstance(width, str):
      width = f"{self._width}px;"
    if CSinSCApp.buffered_mode:
      CSinSCApp.styles[self]["width"] = width
    else:
      self.widget.style["width"] = width

  @property
  def height(self): 
    return self._height
  @height.setter
  def height(self, value): 
    self._height = value

    height = self._height
    if not isinstance(height, str):
      height = f"{self._height}px;"
    if CSinSCApp.buffered_mode:
      CSinSCApp.styles[self]["height"] = height
    else:
      self.widget.style["height"] = height

  @property
  def y(self): 
    return self._y
  @y.setter
  def y(self, value): 
    self._y = value
    if CSinSCApp.buffered_mode:
      CSinSCApp.styles[self]["top"] = f"{self._y}px;"
    else:
      self.widget.style["top"] = f"{self._y}px;"         

  @property
  def visible(self): 
    return self._visible
  @visible.setter
  def visible(self, value): 
    self._visible = value

    if CSinSCApp.buffered_mode:
      CSinSCApp.styles[self]["display"] = "inline;" if self._visible == True else "none;"
    else:
      self.widget.style["display"] = "inline;" if self._visible == True else "none;"

  def _setbgcolor(self, _bgcolor):
    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("background-color", self, f"rgba({_bgcolor.r}, {_bgcolor.g}, {_bgcolor.b}, {_bgcolor.a});"))
    else:
      self.widget.style["background-color"] = f"rgba({_bgcolor.r}, {_bgcolor.g}, {_bgcolor.b}, {_bgcolor.a});"    

  def _setcolor(self, _color):
    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("color", self, f"rgba({_color.r}, {_color.g}, {_color.b}, {_color.a});"))
    else:
      self.widget.style["color"] = f"rgba({_color.r}, {_color.g}, {_color.b}, {_color.a});"         

  @property
  def bgcolor(self): 
    return self._bgcolor
  @bgcolor.setter
  def bgcolor(self, value): 
    if isinstance(value, list):
      c = list(value) + [1]
      self._bgcolor = Color(*c)
    else:
      self._bgcolor = value

    self._bgcolor.parent = self._setbgcolor

    self._setbgcolor(self._bgcolor)

  @property
  def padding(self): 
    return self._padding
  @padding.setter
  def padding(self, value): 
    self._padding = list(value)

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("padding", self, f"{self._padding[0]}px {self._padding[1]}px {self._padding[2]}px {self._padding[3]}px;"))
    else:
      self.widget.style["padding"] = f"{self._padding[0]}px {self._padding[1]}px {self._padding[2]}px {self._padding[3]}px;"

  @property
  def margin(self): 
    return self._margin
  @margin.setter
  def margin(self, value): 
    self._margin = list(value)

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("margin", self, f"{self._margin[0]}px {self._margin[1]}px {self._margin[2]}px {self._margin[3]}px;"))
    else:
      self.widget.style["margin"] = f"{self._margin[0]}px {self._margin[1]}px {self._margin[2]}px {self._margin[3]}px;"      

  @property
  def data(self):
    return self._data
  @data.setter
  def data(self, value):
    self._data = value
    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(FunctionCallCommand(self.widget.set_text, self, value))
    else:
      self.widget.set_text(value)    

  @property
  def color(self): 
    return self._color
  @color.setter
  def color(self, value): 
    if isinstance(value, list):
      c = list(value) + [1]
      self._color = Color(*c)
    else:
      self._color = value

    self._color.parent = self._setcolor

    self._setcolor(self._color)

  @property
  def fontSize(self): 
    return self._fontSize  
  @fontSize.setter
  def fontSize(self, value): 
    # overriding the visible property to "flex" instead of "inline"
    self._fontSize = value

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("font-size", self, f"{self._fontSize}px"))
    else:    
      self.widget.style["font-size"] = f"{self._fontSize}px"

  @property
  def fontFamily(self): 
    return self._fontFamily  
  @fontFamily.setter
  def fontFamily(self, value): 
    # overriding the visible property to "flex" instead of "inline"
    self._fontFamily = value

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("font-family", self, f"{self._fontFamily}"))
    else:    
      self.widget.style["font-family"] = f"{self._fontFamily}"     

  # TODO make this more custom friendly!
  def center(self):
    # full center
    self.widget.style["position"] = "relative;"
    self.widget.style["margin"] = "auto;"
    self.widget.style["left"] =  "0;"
    self.widget.style["right"] =  "0;"
    self.widget.style["top"] =  "0;"
    self.widget.style["bottom"] =  "0;"  

class Label (Control):
  def __init__(self, text = "", x = 0, y = 0, width = 64, height = 32):
    self.widget = gui.Label(text, width = width, height = height)  
    super(Label, self).__init__(x, y, width, height)   

    self._fontSize = "12px"
    self._fontFamily = "arial"

    # centred by default
    self.widget.style["display"] = "flex;"
    self.widget.style["justify-content"] = "center;"
    self.widget.style["align-items"] = "center;"
    self.widget.style["text-align"] = "center;"

  @property
  def visible(self): 
    return self._visible  
  @visible.setter
  def visible(self, value): 
    # overriding the visible property to "flex" instead of "inline"
    self._visible = value

    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(StyleCommand("display", self, "flex;" if self._visible == True else "none;"))
    else:    
      self.widget.style["display"] = "flex;" if self._visible == True else "none;"  

class Button (Control):
  def __init__(self, text = "", x = 0, y = 0, width = 64, height = 32):
    self.widget = gui.Button(text, width = width, height = height)  
    super(Button, self).__init__(x, y, width, height)   

class Image (Control):
  def __init__(self, filename = None, x = 0, y = 0, width = 32, height =  32):
    self.widget = gui.Image('', width = width, height = height)  

    self.widget.attributes['ondragstart'] = "event.preventDefault();"

    super(Image, self).__init__(x, y, width, height)   

    self.cached_filename = None

    if filename is not None and len(filename) > 0:
      self._setData(filename)

  @property
  def data(self):
    return self._data
  @data.setter
  def data(self, value):
    self._data = value
  
    if self._data == self.cached_filename:
      return
      
    if CSinSCApp.buffered_mode:
      CSinSCApp.commands.append(FunctionCallCommand(self._setData, self, self._data))
    else:      
      imageData = CSinSCApp.readResource(self._data)
      self.widget.set_image("data:image/" + imageData[0] + ";base64," + imageData[1].decode("utf-8"))

      self.cached_filename = self._data

  def _setData(self, data):
    imageData = CSinSCApp.readResource(data)
    self.widget.set_image("data:image/" + imageData[0] + ";base64," + imageData[1].decode("utf-8"))

    self.cached_filename = data


class CSinSCApp:
  buffered_mode = False

  resources_cache = {}

  commands = []
  styles = {}

  title = "CSinSchools Application"

  def __init__(self, title = "CSinSchools Application", width = "100%", height = "100%"):
    if title is None or len(title) == 0:
      raise Exception("Please supply a title for the application.")
    self.events = []  
    self.initialised = False

    CSinSCApp.title = title

    self.container = gui.Container(width = width, height = height)   
    self.container.style["display"] = "flex;"
    self.container.style["justify-content"] = "center;"
    self.container.style["align-items"] = "top;"

    self.thread_id = None

  # alias for addControl
  def add(self, control):
    self.addControl(control)

  def addControls(self, controls):
    for control in controls:
      self.addControl(control)

  def addControl(self, control):
    self.container.append(control.widget)
    CSinSCApp.styles[control] = {}
    control.widget.onclick.do(self.on_click, control)
    # BUG in REMI - onmouseover removed from version 2020.3
    #control.widget.onmouseover.do(self.on_mouse_over, control)
    control.widget.onmouseout.do(self.on_mouse_out, control)
    control.widget.onmousemove.do(self.on_mouse_move, control)

  def remi_thread(self):
    start(CSinSCApp.MyApp, title = CSinSCApp.title, debug=False, address='0.0.0.0', port=0, multiple_instance = False, userdata = (self,))    

  def main(self):
    self.initialised = True
    return self.container

  def run(self):
    self.thread_id = Thread(target=self.remi_thread, daemon=True)
    self.thread_id.daemon = True
    self.thread_id.start()

    while not self.initialised:
      pass

  def stop(self):
    if self.thread_id is not None:
      self.thread_id.join()

  def refresh(self, buffer = True):

    CSinSCApp.buffered_mode = buffer
    
    for command in CSinSCApp.commands:
      command.execute()

    # apply all styles
    for control in CSinSCApp.styles.keys():
      for style in CSinSCApp.styles[control].keys():        
        control.widget.style[style] = CSinSCApp.styles[control][style]

    CSinSCApp.commands = []

    #clear styles
    for control in CSinSCApp.styles.keys():
      CSinSCApp.styles[control] = {}

  def readResource(filename):

    if filename in CSinSCApp.resources_cache:
      #print(f"found {filename} in resources cache")
      return CSinSCApp.resources_cache[filename]

    resource_ext = filename.split(".")[-1]

    with open(filename, "rb") as resource:
      encoded_string = base64.b64encode(resource.read())

      CSinSCApp.resources_cache[filename] = (resource_ext, encoded_string)

    return (resource_ext, encoded_string)

  class MyApp(App):
    def __init__(self, *args):
      
      self.window = args[-1].userdata[0]
      
      super(CSinSCApp.MyApp, self).__init__(*args)   

    def main(self, userdata):
      return userdata.main()

  def on_click(self, widget, control):
    self.events.append(Event(CLICK, control))

  def on_mouse_over(self, widget, control):
    self.events.append(Event(MOUSE_OVER, control))    

  def on_mouse_out(self, widget, control):
    self.events.append(Event(MOUSE_OUT, control))

  def on_mouse_down(self, widget, x, y, control):
    self.events.append(Event(MOUSE_DOWN, control, x, y))

  def on_mouse_move(self, widget, x, y, control):
    self.events.append(Event(MOUSE_MOVE, control, x, y))    
  
  def get_next_event(self, event_types = None):
    accept = False
    event = None

    if len(self.events) > 0:
      event = self.events[0]
      del self.events[0]
      if event_types is None:
        accept = True
      elif isinstance(event_types, list):
        if event.type in event_types:
          accept = True
      elif isinstance(event_types, int):
        if event.type == event_types:
          accept = True
          
    if not accept:
      event = Event(None, None)
    return event

  def wait_for_event(self, event_types = None):
    accept = False
    while not accept:
      if len(self.events) == 0:
        continue
      event = self.events[0]
      del self.events[0]
      if event_types is None:
        accept = True
      elif isinstance(event_types, list):
        if event.type in event_types:
          accept = True
      elif isinstance(event_types, int):
        if event.type == event_types:
          accept = True
    return event
      
