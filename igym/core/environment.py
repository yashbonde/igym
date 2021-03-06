# MIT License
#
# Copyright(c) 2021 Yash Bonde
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List
from selenium import webdriver

from igym import Action

class InternetEnv():
  def __init__(self, path_to_chromedriver: str, url = None):
    self.driver = webdriver.Chrome(path_to_chromedriver)
    if url != None:
      self.driver.get(url)

  def close(self):
    self.driver.close()

  def step(self, action: Action = None, actions_list: List[Action] = None):
    if action is None and actions_list is None:
      raise ValueError("Need to provide either `action` of `actions_list`")
    elif action is not None and actions_list is not None:
      raise ValueError("Need to provide either `action` of `actions_list`")

    if actions_list is not None:
      for act in actions_list:
        act.step(self.driver)

    else:
      action.step(self.driver)

