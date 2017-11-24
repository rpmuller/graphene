import xml.etree.ElementTree as ET

class Scene:
    def __init__(self):
        self.items = []
        self.height = 400 # override with bbox calculation
        self.width = 400 # override with bbox calculation
        return

    def _repr_svg_(self): return self.to_svg()    
    def add(self,item): self.items.append(item)
        
    def bbox(self,border=0,BIG=1e10):
        self.xmin = self.ymin = BIG
        self.xmax = self.ymax = -BIG
        for item in self.items:
            xmin,xmax,ymin,ymax = item.bbox()
            self.xmin = min(self.xmin,xmin)
            self.xmax = max(self.xmax,xmax)
            self.ymin = min(self.ymin,ymin)
            self.ymax = max(self.ymax,ymax)
        self.xmin -= border
        self.ymin -= border
        self.xmax += border
        self.ymax += border
        self.height = self.ymax
        self.width = self.xmax
        return
    
    def to_svg(self,border=10,fname=False):
        self.bbox(border)
        svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="1.1",
                        height="%s" % self.height, width="%s" % self.width)
        g = ET.SubElement(svg,"g",style="fill-opacity:1.0; stroke:black; stroke-width:1;")
        for item in self.items:
            item.to_svg(g)
        #ET.dump(svg) # useful for debugging
        if fname:
            open(fname,'w').write(ET.tostring(svg))
        return ET.tostring(svg)

    def line(self,start,end,**kwargs): self.items.append(Line(start,end,**kwargs))
    def circle(self,center,radius,color='blue',linecolor='black'): 
        self.items.append(Circle(center,radius,color,linecolor))
    def rectangle(self,origin,height,width,color='blue',linecolor='black'): 
        self.items.append(Rectangle(origin,height,width,color,linecolor))
    def text(self,origin,text,size=24): self.items.append(Text(origin,text,size))
    
class Line:
    def __init__(self,start,end,dashed=False):
        self.start = start #xy tuple
        self.end = end     #xy tuple
        self.dashed = dashed
        return
    
    def to_svg(self,parent):
        line = ET.SubElement(parent,"line",x1=str(self.start[0]),y1=str(self.start[1]),
                             x2=str(self.end[0]),y2=str(self.end[1]))
        if self.dashed:
            line.set("stroke-dasharray","3,3")
        return

    def bbox(self):
        return min(self.start[0],self.end[0]),max(self.start[0],self.end[0]),\
               min(self.start[1],self.end[1]),max(self.start[1],self.end[1])

class Circle:
    def __init__(self,center,radius,color,linecolor='black'):
        self.center = center #xy tuple
        self.radius = radius #xy tuple
        self.color = color   #rgb tuple in range(0,256)
        self.linecolor = linecolor
        return
    
    def to_svg(self,parent):
        color = colorstr(self.color)
        linecolor = colorstr(self.linecolor)
        ET.SubElement(parent,"circle",cx=str(self.center[0]),cy=str(self.center[1]),
                      r=str(self.radius),style="fill:%s;stroke=%s" % (color,linecolor))

    def bbox(self):
        return self.center[0]-self.radius,self.center[0]+self.radius,\
               self.center[1]-self.radius,self.center[1]+self.radius

class Rectangle:
    def __init__(self,origin,height,width,color,linecolor='black'):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        self.linecolor = linecolor
        return

    def to_svg(self,parent):
        color = colorstr(self.color)
        linecolor = colorstr(self.linecolor)
        ET.SubElement(parent,"rect",x=str(self.origin[0]),y=str(self.origin[1]),
                      height=str(self.height),width=str(self.width),
                      style="fill:%s;stroke-width:1;stroke=%s" % (color,linecolor))

    def bbox(self):
        return self.origin[0],self.origin[0]+self.width,self.origin[1],self.origin[1]+self.height

class Text:
    def __init__(self,origin,text,size=24):
        self.origin = origin
        self.text = text
        self.size = size
        return

    def to_svg(self,parent):
        fs = "font-size"
        el = ET.SubElement(parent,"text",x=str(self.origin[0]),y=str(self.origin[1]))
        el.set("font-size",str(self.size))
        el.text = self.text
    
    def bbox(self):
        return self.origin[0],self.origin[0]+self.size,\
               self.origin[1],self.origin[1]+self.size # Guessing here
    
def colorstr(rgb): 
    if type(rgb) == type(""): return rgb
    #return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)
    return "rgb(%s,%s,%s)" % tuple(rgb)

if __name__ == '__main__':
    scene = Scene()
    scene.rectangle((100,100),200,200,(0,255,255))
    scene.line((200,200),(200,300))
    scene.line((200,200),(300,200))
    scene.line((200,200),(100,200))
    scene.line((200,200),(200,100))
    scene.circle((200,200),30,(0,0,255))
    scene.circle((200,300),30,(0,255,0))
    scene.circle((300,200),30,(255,0,0))
    scene.circle((100,200),30,(255,255,0))
    scene.circle((200,100),30,"fuchsia")
    scene.text((50,50),"Testing SVG")
    scene.to_svg(fname="/Users/rmuller/Desktop/scene.svg")
