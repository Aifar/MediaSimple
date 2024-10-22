import os
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase

resource_add_path(os.path.abspath(".font"))

LabelBase.register("simsun", "./font/simsun.ttf")


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, StringProperty
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.clock import Clock
from moviepy.editor import VideoFileClip

from PIL import Image
import piexif
import imghdr

kvStr = '''
<StatefulLabel>:
    rgba: (1,1,1,1)
    canvas.before:
        Color:
            rgba: self.rgba
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        id: file_name           
        text: root.text
        padding: 10,10,10,10
        color: 0,0,0,1
        size_hint_x: 0.6
        text_size: self.size
        halign: 'left'
        font_name: 'simsun'
    Label:
        id: file_size
        size_hint_x: 0.2
        color: 0,0,0,1
        padding: 10,10,10,10
        text_size: self.size
        halign: 'center'
        text: root.size_text
    Label:
        id: file_saving
        size_hint_x: 0.2
        color: 0,0,0,1
        padding: 10,10,10,10
        text_size: self.size
        halign: 'center'
        text: root.saving_text  
<RV>:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    viewclass: 'StatefulLabel'
    RecycleBoxLayout:
        spacing: 0
        default_size: None, dp(36)
        size_hint_y: None
        default_size_hint: 1, None
        height: self.minimum_height
        orientation: 'vertical'
BoxLayout:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: 0.05
        orientation: 'horizontal'
        Label:       
            text: 'File'
            size_hint_x: 0.6
            color: 0,0,0,1
            padding: 10,10,10,10
            text_size: self.size
            canvas:
                Color:
                    rgba: 0.8,0.8,0.8,1
                Line:
                    rectangle: (self.pos[0], root.height - self.height, self.width, self.height)
                    width: 2
        Label:            
            text: 'Size'
            size_hint_x: 0.2
            color: 0,0,0,1
            padding: 10,10,10,10
            halign: 'center'
            text_size: self.size 
            canvas:
                Color:
                    rgba: 0.8,0.8,0.8,1
                Line:
                    rectangle: (self.pos[0], root.height - self.height, self.width, self.height)
                    width: 2
        Label:            
            text: 'Savings'
            color: 0,0,0,1
            size_hint_x: 0.2
            padding: 10,10,10,10
            text_size: self.size 
            halign: 'center'
            canvas:
                Color:
                    rgba: 0.8,0.8,0.8,1
                Line:
                    rectangle: (self.pos[0], root.height - self.height, self.width, self.height)
                    width: 2         

    RV:
        id: rv
'''


class StatefulLabel(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty()
    size_text = StringProperty()
    saving_text = StringProperty()
    index = 0

    '''
    To change a viewclass' state as the data assigned to it changes,
    overload the refresh_view_attrs function (inherited from
    RecycleDataViewBehavior)
    '''
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        # self.rgba = (0.8,0.8,0.8,1)
        if self.index % 2 == 0:
            self.rgba = (1,1,1,1)
        else:
            self.rgba = (0.96,0.96,0.96,1)
       

        print('refresh_view_attrs ' + str(index))
        super(StatefulLabel, self).refresh_view_attrs(rv, index, data)

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

class MyApp(App):
    data = []
    
    def build(self):
        Window.bind(on_drop_file=self.handledrops)
        self.title = "MediaSimple"
        return Builder.load_string(kvStr)
  

    def handledrops(self, window, filename, x, y):
        path = bytes.decode(filename)
        print(path)

        for pathIn in self.data:
            if pathIn == path:
                return
        basename = os.path.basename(path)
        file_name, file_extension = os.path.splitext(basename)

        print('file_extension: '+file_extension)
        if(file_extension == '.mp4'):
            imageType = file_extension
        else:
            imageType = self.whatImage(path)

        print(imageType)
        if(imageType  !='png' and imageType !='jpeg' and imageType !='gif' and imageType !='webp'  and imageType !='.mp4'):
            return

        stats = os.stat(path)
        print(stats.st_size)
 
        self.data.append(path)
        self.root.ids['rv'].__self__.data.append({'text':basename, 'size_text':str(stats.st_size), 'saving_text':''})
        ind = len(self.root.ids['rv'].__self__.data)-1

        Clock.schedule_once(lambda dt: self.reduceFile(path, basename,imageType,stats.st_size,ind), 1)
        
    def reduceFile(self, path, basename,imageType,st_size,ind):
      
        destFilename = self.getDestFilename(path, basename)
 
        if imageType=='png':
            self.reducePng(path, destFilename)
        elif imageType=='jpeg':
            self.reduceJpg(path, destFilename)
        elif imageType=='gif':
            self.reduceGif(path, destFilename)
        elif imageType=='webp':
            self.reduceWebp(path, destFilename) 
        elif imageType=='.mp4':
            self.reduceMp4(path, destFilename)  

        destStats = os.stat(destFilename)
        saving_text = str(round(((st_size -destStats.st_size)/st_size)*100, 2))
        Clock.schedule_once(lambda dt: self.refreshSavingText(ind, saving_text), 1)
        

    def refreshSavingText(self, ind, text):
        print('ind: '+str(ind) + ' text:' + text + '')
        self.root.ids['rv'].__self__.data[ind]['saving_text'] =  text + '%'
        self.root.ids['rv'].__self__.refresh_from_data()

    def reducePng(self,path, destFilename):
        with Image.open(path) as img:
            img = Image.open(path)
            img_8bit = img.convert("P", palette=Image.ADAPTIVE, colors=256)
            img_8bit.save(destFilename)  
     

    def reduceJpg(self,path, destFilename):
        with Image.open(path) as img:
            img.save(destFilename, quality=90)  
            self.remove_exif(destFilename)     

    def reduceWebp(self,path, destFilename):
        with Image.open(path) as img:
            img.save(savedFilename, quality=90)         

    def remove_exif(self, path):
        piexif.remove(path)

    def reduceGif(self,path, destFilename):
        with Image.open(path) as img:

            frames = []
            for frame_num in range(img.n_frames):
                img.seek(frame_num)
                frame = img.copy()
                img_8bit = frame.convert("P", palette=Image.ADAPTIVE, colors=256)
                frames.append(img_8bit)
      
            gif_save_params = {'optimize': True, 'save_all': True, 'loop': 0}
            frames[0].save(destFilename, format='GIF', append_images=frames[1:], **gif_save_params)
    
    def reduceMp4(self,path, destFilename):
        with VideoFileClip(path) as  video_clip:
            video_clip.write_videofile(destFilename, bitrate='2500K')

    def whatImage(self, path):
        return imghdr.what(path)

    def getDestFilename(self, path, basename):
        directory = os.path.dirname(os.path.abspath(path))
        file_name, file_extension = os.path.splitext(basename)
        destFilename = directory+'/'+file_name+'_opt' + file_extension
        return destFilename


if __name__ == '__main__':
    MyApp().run()