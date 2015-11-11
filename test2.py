#!/usr/bin/env python
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import sys, re, string, numpy as np, matplotlib.pyplot as plt, math as math
import Tkinter as tk
from Tkinter import *
from ScrolledText import ScrolledText

class Demo(Frame):
   def __init__(self, master):
      Frame.__init__(self, master, relief=RAISED, bd=2)
      l = Label(self, text=self.label, font=('Helvetica', 12, 'italic bold'),
              background='dark slate blue', foreground='white')
      l.pack(side=TOP, expand=NO, fill=X)

class ReliefDemo(Demo):
   label = 'Relief types: Label widgets with 2d/3d borders'
   def __init__(self, master):
      Demo.__init__(self, master)
      for relief in [RAISED, SUNKEN, RIDGE, GROOVE, FLAT, SOLID]:
         l = Label(self, text=relief, relief=relief, bd=4)
         l.pack(side=LEFT, expand=YES, fill=BOTH,
               padx=4, pady=4, ipadx=4, ipady=4)

class OptionDemo(Demo):
   label = 'OptionMenu:'
   def __init__(self, master):
      Demo.__init__(self, master)

      f = Frame(self)
      Label(f, text='Incoupling lense').pack(side=LEFT)
      op = OptionMenu(f, app.justifyVar, 'C280TMD-C', 'C220TMD-C', 'A260TM-C', 'A280TM-C', 'A220(no C-coating)','Choose properties manually')
      op.pack()
      f.pack()

      # f = Frame(self)
      # Label(f, text='Fit to').pack(side=LEFT)
      # op = OptionMenu(f, app.sizeVar, 'minimum', 'maximum')
      # op.pack()
      # f.pack()

      

      f1Var = StringVar()
      f = Frame(self)
      Label(f, text='Focal length first lense (mm)').pack(side=LEFT)
      op = Entry(f, textvariable = f1Var)
      op.pack()
      f.pack()
      f1Var.set("")
      s1 = f1Var.get()

      f2Var = StringVar()
      f = Frame(self)
      Label(f, text='Focal length second lense (mm)').pack(side=LEFT)
      op = Entry(f, textvariable = f2Var)
      op.pack()
      f.pack()
      f2Var.set("")
      s2 = f2Var.get()

      x2Var = StringVar()
      f = Frame(self)
      Label(f, text='Position second lense (mm)').pack(side=LEFT)
      op = Entry(f, textvariable = x2Var)
      op.pack()
      f.pack()
      x2Var.set("")
      s3 = x2Var.get()

      ilVar = StringVar()
      f = Frame(self)
      Label(f, text='Position incoupling lense').pack(side=LEFT)
      op = Entry(f, textvariable = ilVar)
      op.pack()
      f.pack()
      ilVar.set("")
      s4 = ilVar.get()




class CanvasDemo(Demo):
   label = 'Canvas widget with simple animation:'
   def __init__(self, master):
      Demo.__init__(self, master)
      self.canvas = Canvas(self, relief=SUNKEN, bd=2, background='gray65',
                      width=100, height=100)
      self.canvas.pack(side=TOP, expand=YES, fill=BOTH)
      self.arc = self.canvas.create_arc(0,0, 1,1)

      self.start, self.extent = 90,0

   def configure(self, event=None):
      fillColor = ''
      if app.fillVar.get(): fillColor = app.colorVar.get()

      outlineColor = ''
      if app.outlineVar.get(): outlineColor = 'black'
      
      self.canvas.itemconfigure(self.arc, style=app.styleVar.get())
      self.canvas.itemconfigure(self.arc, fill=fillColor)
      self.canvas.itemconfigure(self.arc, outline=outlineColor)
      
    # ----------------------------------------------------------------
    #        simply draws a thin-lens at the provided location
    # parameters:
    #     - z:    location along the optical axis (in mm)
    #     - f:    focal length (in mm, can be negative if div. lens)
    #     - diam: lens diameter in mm
    #     - lbl:  label to identify the lens on the drawing
    # ----------------------------------------------------------------
   def add_lens(self, a, z, f, diam, lbl):
      ww, tw, rad = diam / 12.0, diam/3.0, diam / 2.0
      a.plot([z, z],    [-rad, rad],                'k', linewidth=2)
      a.plot([z, z+tw], [-rad, -rad+np.sign(f)*ww], 'k', linewidth=2)
      a.plot([z, z-tw], [-rad, -rad+np.sign(f)*ww], 'k', linewidth=2)
      a.plot([z, z+tw], [ rad,  rad-np.sign(f)*ww], 'k', linewidth=2)
      a.plot([z, z-tw], [ rad,  rad-np.sign(f)*ww], 'k', linewidth=2)
      #plt.plot([z+f, z+f], [-ww,ww], 'k', linewidth=2)
      #plt.plot([z-f, z-f], [-ww,ww], 'k', linewidth=2)
      a.text(z,rad+5.0, lbl, fontsize=10)
      if (f == float("inf")):   a.text(z,rad+2.0, 'mirror', fontsize=8)  
      else:       a.text(z,rad+2.0, 'f='+str(int(f))+' mm', fontsize=8)


   def animate(self):
      w,h = self.canvas.winfo_width(), self.canvas.winfo_height()

      w  = 0
      h = 0

      # if app.sizeVar.get() == 'minimum':
      #    s = min(w,h)
      # else:
      #    s = max(w,h)

      # if app.justifyVar.get() == 'left':
      #    x0,x1 = 10, s-10
      # elif app.justifyVar.get() == 'center':
      #    x0,x1 = (w-s+20)/2, (w+s-20)/2
      # else:
      #    x0,x1 = w-s+10, w-10

      # y0, y1 = (h-s+20)/2, (h+s-20)/2



      #plt.clf()
 
      zmin, zmax       = -10., 456.
      xmin, xmax       = -25, 25
      bignum, smallnum = 1e6, 1e-6   # all distances expressed in mm
       
      # ------------------------------------
      #   location + focal length of optics
      # ------------------------------------
      zl = np.array([40.0, 170.0, 230.0, 385.0])#, 1000.0, 1200.0, 1342.0]) # lens positions
      ffred = np.array([float("inf"), float("inf"), float("inf"), 18.24]) #IL_f_637])#,  100.0,  100.0,   35.0]) # lens focal length
      ffinfrared = np.array([40.0, 80.0, float("inf"), 18.58])
       
      xsrc, zsrc, zpup = 2.0 , 0.0, -bignum # position of src and pupil
      srcpos = (zsrc, xsrc)
       
      #  draw the different beams
      # --------------------------
      #propagate_beam(srcpos,          4, 500, zl, ff, 'src1', 'b')
      #propagate_beam((0.0, -2.),      4,  20, zl, ff, 'src1', 'r')
      #propagate_beam((zpup,),    0.0005,  2, zl, ffinfrared, 'src1', 'g')
      #propagate_beam((zpup,),    0.0005*2.1,  2, zl, ffred, 'src1', 'r')
      #propagate_beam((110,),          2,  40, zl, ff, 'DM',   'y')
       
      #  print a couple labels
      # --------------------------
      #plt.text(0, 20, 'src 1', bbox=dict(facecolor='blue', alpha=1), fontsize=10)
      #plt.text(0, 17, '637 nm source', bbox=dict(facecolor='red',  alpha=1), fontsize=10)
      #plt.text(0, 14, '1064 nm source', bbox=dict(facecolor='green',  alpha=1), fontsize=10)
      #plt.text(0, 11, 'DM', bbox=dict(facecolor='yellow',  alpha=1), fontsize=10)
       
      #      add the lenses
      # -------------------------

      f = Figure(figsize=(3,3), dpi=100)
      a = f.add_subplot(111)
      #a.plot([zmin,zmax], [0,0], 'k')
      a.axis([zmin,zmax, xmin, xmax])

      names = ["L1", "L2", "DM", "IL"]
      for i in range(np.size(zl)): self.add_lens(a, zl[i], ffinfrared[i], 25, names[i])



      #a.title("Example of brilliant optical design!")

      

      canvas = FigureCanvasTkAgg(f, self)
      canvas.show()
      canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

      toolbar = NavigationToolbar2TkAgg(canvas, self)
      toolbar.update()
      canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
       
      #     plot optical axis
      # -------------------------
      # plt.plot([zmin,zmax], [0,0], 'k')
      # plt.axis([zmin,zmax, xmin, xmax])
      # #plt.axis([zmin+412,zmax, xmin+23, xmax-23])
      # plt.title("Example of brilliant optical design!")
      # plt.show()

      #self.canvas.coords(self.arc, x0,y0, x1,y1)
      #self.start  = self.start  - app.animateSpeed1.get()
      #self.extent = self.extent - app.animateSpeed2.get()
      #self.canvas.itemconfigure(self.arc,start=self.start,extent=self.extent)
      #root.after(10, self.animate)

# A small collection (about 16%) of the colors found in the usual X11 color
# data base:  .../lib/X11/rgb.txt

COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white',
        'old lace', 'linen', 'antique white', 'papaya whip',
        'blanched almond', 'bisque', 'peach puff', 'navajo white',
        'moccasin', 'cornsilk', 'ivory', 'lemon chiffon', 'seashell',
        'honeydew', 'mint cream', 'azure', 'alice blue', 'lavender',
        'lavender blush', 'misty rose', 'white', 'black', 'dark slate gray',
        'dark slate grey', 'dim gray', 'dim grey', 'slate gray',
        'slate grey', 'light slate gray', 'light slate grey', 'gray',
        'grey', 'light grey', 'light gray', 'midnight blue', 'navy',
        'navy blue', 'cornflower blue', 'dark slate blue', 'slate blue',
        'medium slate blue', 'light slate blue', 'medium blue',
        'royal blue', 'blue', 'dodger blue', 'deep sky blue', 'sky blue',
        'light sky blue', 'steel blue', 'light steel blue', 'light blue',
        'powder blue', 'pale turquoise', 'dark turquoise',
        'medium turquoise', 'turquoise', 'cyan', 'light cyan', 'cadet blue',
        'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
        'dark sea green', 'sea green', 'medium sea green',
        'light sea green', 'pale green', 'spring green', 'lawn green',
        'green', 'chartreuse', 'medium spring green', 'green yellow',
        'lime green', 'yellow green', 'forest green', 'olive drab',
        'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
        'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod',
        'dark goldenrod', 'rosy brown', 'indian red', 'saddle brown',
        'sienna', 'peru', 'burlywood', 'beige', 'wheat', 'sandy brown',
        'tan', 'chocolate', 'firebrick', 'brown', 'dark salmon', 'salmon',
        'light salmon', 'orange', 'dark orange', 'coral', 'light coral',
        'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink',
        'light pink', 'pale violet red', 'maroon', 'medium violet red',
        'violet red', 'magenta', 'violet', 'plum', 'orchid',
        'medium orchid', 'dark orchid', 'dark violet', 'blue violet',
        'purple', 'medium purple', 'thistle', 'dark grey', 'dark gray',
        'dark blue', 'dark cyan', 'dark magenta', 'dark red', 'light green']

COLORS.sort(lambda a,b: cmp(string.split(a)[-1], string.split(b)[-1]))

class ListboxDemo(Demo):
   label = 'Listbox, Entry, Button,\nand Scrollbar widgets:'
   def __init__(self, master):
      Demo.__init__(self, master)

      e = Entry(self, textvariable=app.colorVar)
      e.pack(side=TOP, fill=X)
      e.bind('<Return>', self.enterColor)
      
      b = Button(self, text='Select color', command=self.selectColor)
      b.pack(side=BOTTOM, fill=X)
      
      self.colorList = Listbox(self, height=6)
      self.colorList.pack(side=LEFT, expand=YES, fill=BOTH)
      for color in COLORS:
         self.colorList.insert(AtEnd(), color)
      self.colorList.selection_set(COLORS.index(app.colorVar.get()))

      scrollbar = Scrollbar(self)
      self.colorList.configure(yscrollcommand=(scrollbar, 'set'))
      scrollbar.configure(command=(self.colorList, 'yview'))
      scrollbar.pack(side=LEFT, fill=Y)

      self.colorList.bind("<Double-Button-1>", self.selectColor)

   def enterColor(self, event=None):
      app.canvasDemo.configure()

   def selectColor(self, event=None):
      colorIndex = map(string.atoi, app.listDemo.colorList.curselection())
      if not colorIndex: return
      app.colorVar.set(app.listDemo.colorList.get(colorIndex[0]))
      app.canvasDemo.configure()

def Char(c): return '0.0+%d char' % c
def Options(**kw): return kw

class TextDemo(Demo):
   label = 'Text widget displaying source with cheap syntax highlighting:\n'+\
         '(Move mouse over text and watch indent-structure highlighting.)'
   font = ('Courier', 10, 'normal')
   bold = ('Courier', 10, 'bold')
   Highlights = {'#.*': Options(foreground='red'),
              r'\'.*?\'': Options(foreground='yellow'),
              r'\bdef\b\s.*:':Options(foreground='blue', spacing1=2),
              r'\bclass\b\s.*\n':Options(background='pink', spacing1=5),
              r'\b(class|def|for|in|import|from|break|continue)\b':
               Options(font=bold)
              }
   
   def __init__(self, master):
      Demo.__init__(self, master)
      self.text = ScrolledText(self, width=80, height=20,
                         font=self.font, background='gray65',
                         spacing1=1, spacing2=1, tabs='24')
      self.text.pack(side=TOP, expand=YES, fill=BOTH)

      content = open(sys.argv[0], 'r').read()
      self.text.insert(AtEnd(), content)

      reg = re.compile('([\t ]*).*\n')
      pos = 0
      indentTags = []
      while 1:
         match = reg.search(content, pos)
         if not match: break
         indent = match.end(1)-match.start(1)
         if match.end(0)-match.start(0) == 1:
            indent = len(indentTags)
         tagb = 'Tagb%08d' % match.start(0)
         tagc = 'Tage%08d' % match.start(0)
         self.text.tag_configure(tagc, background='', relief=FLAT, borderwidth=2)
         self.text.tag_add(tagb, Char( match.start(0)), Char(match.end(0)))
         self.text.tag_bind(tagb, '<Enter>',
                        lambda e,self=self,tagc=tagc: self.Enter(tagc))
         self.text.tag_bind(tagb, '<Leave>',
                        lambda e,self=self,tagc=tagc: self.Leave(tagc))
         del indentTags[indent:]
         indentTags.extend( (indent-len(indentTags))*[None] )
         indentTags.append(tagc)
         for tag in indentTags:
            if tag:
               self.text.tag_add(tag, Char(match.start(0)),
                             Char(match.end(0)))
         pos = match.end(0)

      for key,kw in self.Highlights.items():
         self.text.tag_configure(key, cnf=kw)
         reg = re.compile(key)
         pos = 0
         while 1:
            match = reg.search(content, pos)
            if not match: break
            self.text.tag_add(key, Char(match.start(0)),Char(match.end(0)))
            pos = match.end(0)

   def Enter(self, tag):
      self.text.tag_raise(tag)
      self.text.tag_configure(tag, background='gray80', relief=RAISED)

   def Leave(self, tag):
      self.text.tag_configure(tag, background='', relief=FLAT)

MessageText = '''All the controls in this block control some aspect of the animation in the Canvas widget.  Most should be self explanitory.  To choose the fill color, do one of (a) type a color name into the Entry widget and RETURN, (b) select a color in the Listbox and hit "Select color" Button, or (c) double-click a color in the Listbox.'''

class MessageDemo(Demo):
   label = 'Message widget:'
   def __init__(self, master):
      Demo.__init__(self, master)
      self.message =  Message(self, text=MessageText)
      self.message.pack(side=TOP, expand=YES, fill=BOTH)
      self.message.bind('<Configure>', self.redoAspectRatio)
   def redoAspectRatio(self, event=None):
      w,h = self.message.winfo_width(), self.message.winfo_height()
      self.message.configure(aspect=(100*w)/h)

# class RadiobuttonDemo(Demo):
#    label = 'Radiobutton:'
#    def __init__(self, master):
#       Demo.__init__(self, master)
#       self.count = IntVar()
#       self.count.set(1)
#       Radiobutton(self, text='Pie Slice',
#                variable=app.styleVar, value='pieslice',
#                command=app.canvasDemo.configure).pack(anchor=W)
#       Radiobutton(self, text='Chord',
#                variable=app.styleVar, value='chord',
#                command=app.canvasDemo.configure).pack(anchor=W)
#       Radiobutton(self, text='Arc only',
#                variable=app.styleVar, value='arc',
#                command=app.canvasDemo.configure).pack(anchor=W)
   
class CheckbuttonDemo(Demo):
   label = 'Which parameters do you want to optimize (max 2)?:'
   def __init__(self, master):
      Demo.__init__(self, master)
      Checkbutton(self, text='Focal length incoupling lense', variable=app.fillVar,
               command=app.canvasDemo.configure).pack(anchor=W)
      Checkbutton(self, text='Focal length first lense telescope', variable=app.outlineVar,
               command=app.canvasDemo.configure).pack(anchor=W)
      Checkbutton(self, text='Focal length second lense telescope', variable=app.outlineVar,
               command=app.canvasDemo.configure).pack(anchor=W)
      Checkbutton(self, text='Position second lense', variable=app.outlineVar,
               command=app.canvasDemo.configure).pack(anchor=W)
      Checkbutton(self, text='Position incoupling lense', variable=app.outlineVar,
               command=app.canvasDemo.configure).pack(anchor=W)

class ScaleDemo(Demo):
   label = 'Scale:\n(animation speed)'
   def __init__(self, master):
      Demo.__init__(self, master)
      s1 = Scale(self, from_=-6.0, to=6.0,
               resolution=0.1,
               label='Start angle increment:',
               orient=HORIZONTAL,
               variable=app.animateSpeed1)
      s1.pack(side=TOP, expand=YES, fill=X)
      s2 = Scale(self, from_=-6.0, to=6.0,
               resolution=0.1,
               label='Extent angle increment:',
               orient=HORIZONTAL,
               variable=app.animateSpeed2)
      s2.pack(side=TOP, expand=YES, fill=X)

class MenubarDemo:

   def __init__(self, master):
      # Create the menu widgets, and register with their parents.
      menubar = Menu(root)
      master.config(menu=menubar)
   
      controlmenu = Menu(menubar)
      menubar.add_cascade(label='Controls', menu=controlmenu)
      
      radiomenu = Menu(menubar)
      controlmenu.add_cascade(label='Radiobutton menu', menu=radiomenu)
   
      checkmenu = Menu(menubar)
      controlmenu.add_cascade(label='Checkbutton menu', menu=checkmenu)
   
      # Add the command(s) to the menu(s)
      controlmenu.add_command(label='Exit', foreground='red',
                        command=sys.exit)

      radiomenu.add_radiobutton(label='Pie Slice', command=self.notify,
                          variable=app.styleVar, value='pieslice')
      radiomenu.add_radiobutton(label='Chord', command=self.notify,
                          variable=app.styleVar, value='chord')
      radiomenu.add_radiobutton(label='Arc only', command=self.notify,
                          variable=app.styleVar, value='arc')

      checkmenu.add_checkbutton(label='Fill', command=self.notify,
                          variable=app.fillVar, onvalue=1, offvalue=0)
      checkmenu.add_checkbutton(label='Outline', command=self.notify,
                          variable=app.outlineVar,onvalue=1,offvalue=0)
         
                      
   def notify(self):
      app.canvasDemo.configure()

                     
   

class Application:
   def __init__(self):
      root.title('tkDemo: Demonstration of Tk widgets')
      root.attributes('-fullscreen', True)
      self.styleVar = StringVar();      self.styleVar.set('pieslice')
      self.fillVar = BooleanVar();      self.fillVar.set(1)
      self.outlineVar = BooleanVar();      self.outlineVar.set(1)
      self.animateSpeed1 = DoubleVar();   self.animateSpeed1.set(1.0)
      self.animateSpeed2 = DoubleVar();   self.animateSpeed2.set(1.0)
      self.colorVar = StringVar();      self.colorVar.set('aquamarine')
      self.justifyVar = StringVar();      self.justifyVar.set('A280TM-C')
      self.sizeVar = StringVar();         self.sizeVar.set('minimum')
      
   def Go(self):
      MenubarDemo(root)
      self.reliefDemo = ReliefDemo(root)
      self.messageDemo = MessageDemo(root)
      self.canvasDemo = CanvasDemo(root)
      self.optionDemo = OptionDemo(root)
      self.listDemo = ListboxDemo(root)
      #self.radioDemo = RadiobuttonDemo(root)
      self.checkDemo = CheckbuttonDemo(root)
      self.scaleDemo = ScaleDemo(root)
      self.textDemo = TextDemo(root)

      self.PackAll(
      [
         [[self.reliefDemo]],
         [[self.messageDemo,self.listDemo,self.scaleDemo],
          [self.canvasDemo,self.checkDemo,self.optionDemo]],#self.radioDemo,self.checkDemo,self.optionDemo]],
         [[self.textDemo]]
      ])

      self.canvasDemo.configure()
      self.canvasDemo.animate()
      
      root.mainloop()

   def PackAll(self, batches):
      for batch in batches:
         b = Frame(root, bd=15, relief=FLAT)
         for row in batch:
            f = Frame(b)
            for widget in row:
               widget.pack(in_=f, side=LEFT, expand=YES, fill=BOTH)
               widget.tkraise()
            f.pack(side=TOP, expand=YES, fill=BOTH)
         b.pack(side=TOP, expand=YES, fill=BOTH)

root = Tk()

if __name__ == '__main__':
   app = Application()
   app.Go()
