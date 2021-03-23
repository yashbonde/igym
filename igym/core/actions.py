import re
from typing import Dict, Tuple, List
from selenium.webdriver.common.keys import Keys
from igym.selenium_utils import elements

from igym.selenium_utils.elements import gather_all_attributes_for_element, IgymElement

format_re = re.compile(r'(\{\w*\})')

class Action:
  def __init__(self, text) -> None:
    self.text = text
    args = [x[1:-1] for x in re.findall(format_re, text)]
    self.args = {x:None for x in args if x}
    self._values_filled = False

  def fill_values(self, **kwargs):
    req_args = set(self.args.keys())
    extra_args = set()
    for k,v in kwargs.items():
      if k not in self.args:
        extra_args.add(k)
      else:
        self.args[k] = v
        req_args.remove(k)

    assert len(req_args) == 0, f"data for following arguments was not found: {req_args}"
    assert len(extra_args) == 0, f"following extra arguments were found: {extra_args}"

    self._values_filled = True

  def __repr__(self) -> str:
    t = self.text
    if self._values_filled:
      t = t.format(**self.args)
    return f"<igym.Action.{self.__class__.__name__}: '{t}'>"


  def get_attributes_of_element(self, driver, element):
    attrs = {}
    # attrs["_element"] = element
    attrs["attr"] = gather_all_attributes_for_element(driver, element)
    attrs["html"] = element.get_property("outerHTML")
    attrs["location"] = element.location
    attrs["text"] = element.text
    attrs["tag"] = element.tag_name
    attrs["url"] = driver.current_url
    elem = IgymElement(**attrs)
    return {elem._hash(): elem}


  def __call__(self, driver) -> Tuple[List, List]:
    """function that wraps the .step() function and caches the attributes
    and HTML of each element"""
    if self._values_filled is False:
      raise ValueError(f"Fill data for action first: {self.__repr__()}")

    items_from_actions = self.step(driver)

    attr = {}
    if items_from_actions is None:
      # this is when action does not return anything
      pass

    elif isinstance(items_from_actions, list) and len(items_from_actions) > 0:
      # when multiple elements are returned
      for element in items_from_actions:
        item = self.get_attributes_of_element(driver, element)
        attr.update(item)

    elif isinstance(items_from_actions, driver._web_element_cls):
      # this is a single element returned
      item = self.get_attributes_of_element(driver, items_from_actions)
      attr.update(item)

    return attr

  def step(self) -> None:
    # this function is called by controller and to be implemented by user
    raise NotImplementedError()


# Base classes, applicable generally

class OpenLink(Action):
  def __init__(self, text = "Open the following URL: '{url}'"):
    super().__init__(text=text)

  def step(self, driver):
    args = self.args
    driver.get(args["url"]) # open this url


class SearchGoogleForText(Action):
  def __init__(self, text="Command for searching {yolo} on Google.com"):
    super().__init__(text=text)

  def step(self, driver):
    args = self.args
    driver.get(f"https://www.google.com?q=" + args["yolo"])  # open this url


class TypeInput(Action):
  def __init__(self, text = "Type the following '{text}' in the first input box"):
    super().__init__(text = text)

  def step(self, driver):
    args = self.args

    curr_url = driver.current_url
    if "google" in curr_url: # weird subroutine for google
      ele = driver.find_element_by_name("q")
    else:
      ele = driver.find_element_by_tag_name("input")
    ele.send_keys(args["text"])
    return ele


class TypeInputAndPressEnter(Action):
  def __init__(self, text="Type the following '{text}' in the first input box and press Enter"):
    super().__init__(text = text)

  def step(self, driver):
    args = self.args

    curr_url = driver.current_url
    if "google" in curr_url: # weird subroutine for google
      ele = driver.find_element_by_name("q")
    else:
      ele = driver.find_element_by_tag_name("input")
    ele.send_keys(args["text"])
    ele.send_keys(Keys.ENTER)
    return None

  
class GetElementsWithTag(Action):
  def __init__(self, text = "Get all web elements on page with tag '{tag}'"):
    super().__init__(text = text)

  def step(self, driver):
    args = self.args
    elements = driver.find_elements_by_tag_name(args["tag"])
    return elements

class ClickElementByPartialLinkText(Action): 
  def __init__(self, text = "Find first element on page with partial text '{text}' and click on it"):
    super().__init__(text = text)

  def step(self, driver):
    element = driver.find_element_by_partial_link_text(self.args["text"])
    element.click()
    return element


# create a list that can be given to the user
DefaultActions = [
  OpenLink(),
  TypeInput(),
  TypeInputAndPressEnter(),
  GetElementsWithTag(),
  ClickElementByPartialLinkText()
]

DefaultActionsUnInit = [
  OpenLink,
  TypeInput,
  TypeInputAndPressEnter,
  GetElementsWithTag,
]
