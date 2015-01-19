#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib2
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4.kdeui import *
from PyKDE4 import plasmascript

from settings import *
from resources import *


"""
  Describes Applet state
  There are two of them:
    USD - display information about usd excahge rate in the
          reguion. Enabled by default
    EUR - same for euro
"""
class State:
  USD = 'usd'
  EUR = 'eur'


"""
  There must be at least one such class, that extends Applet class
  Name doesnt' matter: in this case it's MainApplet
"""
class MainApplet(plasmascript.Applet):
  def __init__(self,parent,args=None):
    plasmascript.Applet.__init__(self,parent)

  def init(self):

    # Set default state (usd by default):
    self.state = State.USD

    # Tuple, that contains prerendered text info for currencies
    self.data = render(get_currency_exchange_rate())

    self.setHasConfigurationInterface(False)
    # It's pretty laggy without this option. So, let it be
    self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

    # Defines widget default size
    # Defines the same size for Minimum and Maximum size
    self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    self.setMinimumSize(applet_width, applet_height)
    self.setMaximumSize(applet_width, applet_height)

    self.timer = self.startTimer(update_interval)

    """ GUI is defined here """
    layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
    font = QFont(font_face, font_size)

    # Loads picture for currency
    self.flag = Plasma.IconWidget()
    self.flag.setIcon(get_image_path(self.state + ".svg"))
    self.flag.setMaximumIconSize(QSizeF(20, 15))
    self.connect(self.flag, SIGNAL('clicked()'), self.on_flag_icon_click)

    # A text label with currency exchange rate
    self.label = Plasma.Label(self.applet)
    self.label.setText(self.data[0])
    self.label.setFont(font)

    # Adding elements to the widget
    layout.addItem(self.flag)
    layout.addItem(self.label)

    # Setting global layout
    self.applet.setLayout(layout)


  def timerEvent(self, ev):
    """ Updates widget text every $TIME_INTERVAL """
    self.data = render(get_currency_exchange_rate())
    self.label.setText(self.data[0] if self.state == State.USD else seld.data[1])

  def on_flag_icon_click(self):
    # todo implement state change
    if self.state == State.USD:
      self.state = State.EUR
      self.label.setText(QString(self.data[1]))
    else:
      self.state = State.USD
      self.label.setText(QString(self.data[0]))

    self.flag.setIcon(get_image_path(self.state + ".svg"))


#  def constraintsEvent(self, constraints):
#    if constraints & Plasma.SizeConstraint:
#      self.resize(self.size())




def CreateApplet(parent):
  """ The function, that starts the widget """
  return MainApplet(parent)



def get_currency_exchange_rate():

  """ Returns string representation of webpage's html """
  html = urllib2.urlopen(website).read().decode('cp1251')

  """ Decimal separated by ',' located between angle braces of closing and opening tag """
  pattern = ">(\\d+,\\d+)<"

  """ Returns list of matched stuff - actually it will be a list courses of euro and usd"""
  both_currencies = re.compile(pattern).findall(html)

  """
    @return (usd, eur) tuple where usd and tuple are lists where:
      - the first element is Central Bank's course
      - the second is the best sell option in the region
      - the third is the best buy option
    USD is every second element, since the first one
    EUR is evey second elemend, since the second one
  """
  return both_currencies[0::2], both_currencies[1::2]

  #def update_usd_exchange_rate():
  #  """Returns annotated exchange rate for USD"""
  #  return with_annotations(get_usd(usd_and_eur_mixed))

  #def update_euro_exchange_rate():
  #  return with_annotations(get_eur(usd_and_eur_mixed))
  #return update_usd_exchange_rate()

#  return QString(u"ЦБ: ").append(xchge_rates[0]).append(QString(u" ")).append(xchge_rates[1]).append(QString(u"/")).append(xchge_rates[2])

def render(usdAndEur):
  return map(
    lambda currencyInfo: QString(u"ЦБ: ").append(currencyInfo[0]).append(u" ").append(currencyInfo[1]).append(u"/").append(currencyInfo[2]),
    usdAndEur
  )



  #return
