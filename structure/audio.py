import pygame as pg


class SoundPathEnum:
  MENU_MUSIC = '../media/music.ogg'
  LEVEL_MUSIC = '../media/'
  STICK_HIT = '../media/hit.ogg'


class Audio:

  def __init__(self):
    self.control = True
    pg.mixer.init(48000, -16, 2, 1024)
    self.p = pg.mixer.Sound('../media/steps.mp3')
    self.channels = [pg.mixer.Channel(0), pg.mixer.Channel(1)]
    self.currentChannel = self.channels[0]


  # The following methods are in charge of managing the music
  def startSound(self):
    pg.mixer.music.play(-1)

  def stopMusic(self):
    pg.mixer.music.stop()

  def change_track(self, track):
    pg.mixer.music.stop()
    pg.mixer.music.unload()
    pg.mixer.music.load(track)

  def play_track(self):
    pg.mixer.music.play(-1)

  def turnUpVolume(self):
    volume = pg.mixer.music.get_volume()
    pg.mixer.music.set_volume(volume+0.10 if volume >= 1 else 1)

  def turnDownVolume(self):
    volume = pg.mixer.music.get_volume()
    pg.mixer.music.set_volume(volume-0.10 if volume <= 0 else 0)


  # The following methods are in charge of managing the sounds like hits, etc

  def loadSound(self, track):
    return pg.mixer.Sound(track)

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
    pass

  def end_rewinded(self):  # stop playing music backwards and play it normally
    pass
