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

