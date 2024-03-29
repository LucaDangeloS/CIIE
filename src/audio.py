import pygame as pg


class SoundPathEnum:
  MENU_MUSIC = '../media/music.ogg'
  LEVEL_MUSIC = '../media/'
  STICK_HIT = '../media/hit.ogg'


class Audio:

  currentSong = ''
  positionOriginal = 0
  invertPath = "../media/invert/"
  normalPath = "../media/"
  controlRewind = True


  def __init__(self):
    self.control = True
    pg.mixer.init(48000, -16, 2, 1024)
    self.p = pg.mixer.Sound('../media/steps.ogg')
    self.channels = [pg.mixer.Channel(0), pg.mixer.Channel(1)]
    self.currentChannel = self.channels[0]
    #Default value of the music
    pg.mixer.music.set_volume(0.3)
    #Default value of the sounds
    for i in range(0,len(self.channels)):
      pg.mixer.Channel(i).set_volume(0.3)


    self.songsDurations = [
      pg.mixer.Sound('../media/music.mp3').get_length(), 
      pg.mixer.Sound('../media/level1Music.mp3').get_length(),
      pg.mixer.Sound('../media/level2Music.mp3').get_length(),
      pg.mixer.Sound('../media/level3Music.mp3').get_length(),
    ]
    # self.songsDurations = [menuMusic,level1Music]
    self.positionOriginal = 0

  # The following methods are in charge of managing the music
  def startMusic(self):
    pg.mixer.music.play(-1)

  def stopMusic(self):
    pg.mixer.music.stop()

  def change_track(self, track):
    pg.mixer.music.stop()
    pg.mixer.music.unload()
    pg.mixer.music.load('../media/'+track)
    self.currentSong = track

  # def load_track(self):
  #   pg.mixer.music.stop()
  #   pg.mixer.music.unload()
  #   pg.mixer.music.load(self.sonsPaths[-1])

  def play_track(self):
    pg.mixer.music.play(-1)

  #Type is a boolean variable used to know if music or sounds (steps, beats, ...) are controlled.
  def getVolume(self, type):
    if type:
      return round(pg.mixer.music.get_volume(),1)
    else: 
      for i in range(0,len(self.channels)):
        return round(pg.mixer.Channel(i).get_volume(),1)

  def turnUpVolume(self,type):
    if type:
      pg.mixer.music.set_volume((pg.mixer.music.get_volume())+0.10)
    else: 
      for i in range(0,len(self.channels)):
        pg.mixer.Channel(i).set_volume((pg.mixer.Channel(i).get_volume())+0.10)
    

  def turnDownVolume(self, type):
    if type:
      pg.mixer.music.set_volume((pg.mixer.music.get_volume())-0.10)
      if pg.mixer.music.get_volume() < 0.090 : pg.mixer.music.set_volume(0.0)
    else: 
      for i in range(0,len(self.channels)):
        pg.mixer.Channel(i).set_volume((pg.mixer.Channel(i).get_volume())-0.10)
        if (pg.mixer.Channel(i).get_volume()) < 0.090 : pg.mixer.Channel(i).set_volume(0.0)


  # The following methods are in charge of managing the sounds like hits, etc

  def loadSound(self, track):
    return pg.mixer.Sound(track)

  #self.walk_sound = self.director.audio.loadSound('../media/steps.ogg')

  def playSound(self, sound, loop=-1):
    if self.control:
      self.currentChannel.play(sound, loop)
      self.control = False

  def stopSound(self, sound):
    pg.mixer.Sound.stop(sound)
    self.control = True

  def setChannel(self, channel):
    self.currentChannel = self.channels[channel]


  def playAttackSound(self, sound):
    self.channels[1].play(sound, 0)

  def start_rewinded(self):  # start playing the music backwards (when you use the clock)
    
    if self.controlRewind:
      self.positionOriginal = (self.positionOriginal + pg.mixer.music.get_pos()/1000.0)%self.songsDurations[self._getSongIndex()]
      pg.mixer.music.stop()
      pg.mixer.music.unload()
      pg.mixer.music.load(f"{self.invertPath}{self.currentSong}")

      start = self.songsDurations[1]- self.positionOriginal

      pg.mixer.music.play(-1, start)
      self.controlRewind = False

  def end_rewinded(self):  # stop playing music backwards and play it normally
    if not self.controlRewind:
      self.controlRewind = True  
      currentPos = pg.mixer.music.get_pos()/1000.0
      pg.mixer.music.stop()
      pg.mixer.music.unload()
      pg.mixer.music.load(f"{self.normalPath}{self.currentSong}")

      start = self.positionOriginal-currentPos
      self.positionOriginal = (self.positionOriginal - currentPos)%self.songsDurations[self._getSongIndex()]

      pg.mixer.music.play(-1, start)

  def _getSongIndex(self):
    if (self.currentSong == 'music.mp3'):
      return 0
    if (self.currentSong == 'level1Music.mp3'):
      return 1
    if (self.currentSong == 'level2Music.mp3'):
      return 2
    if (self.currentSong == 'level3Music.mp3'):
      return 3
