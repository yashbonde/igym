from typing import List
from selenium import webdriver

from igym import Action

class InternetEnv():
  def __init__(self, path_to_chromedriver: str, url = None):
    self.driver = webdriver.Chrome(path_to_chromedriver)
    if url != None:
      self.driver.get(url)
    
    self.step_counter = 0 # this counter is incremented everytime an action is completed
    self.current_url = None
    self.reset_for_new_page()

  def close(self):
    self.driver.close()

  def reset_for_new_page(self):
    self.elements = {}

  def _register_element(self, element):
    if element is not None:
      self.elements.update(element)
    self.step_counter += 1

  def step(
    self,
    action: Action = None,
    actions_list: List[Action] = None,
    output_attrs: bool = False,
  ):
    if action is None and actions_list is None:
      raise ValueError("Need to provide either `action` of `actions_list`")
    elif action is not None and actions_list is not None:
      raise ValueError("Need to provide either `action` of `actions_list`")

    if actions_list is not None:
      attrs = []
      for action in actions_list:
        attr = action(self.driver)
        self._register_element(attr)
        attrs.append(attr)
    else:
      attr = action(self.driver)
      self._register_element(attr)
      attrs = [attr]
  
    output = []
    if output_attrs:
      output += attrs

    new_url = self.driver.current_url
    if new_url != self.current_url:
      self.reset_for_new_page()
      self.current_url = new_url

    return output
