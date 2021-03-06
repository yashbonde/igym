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

import re
from selenium.webdriver.common.keys import Keys

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

    self._values_filled

  def __repr__(self) -> str:
    return f"<igym.Action.{self.__class__.__name__}: '{self.text.format(**self.args)}'>"

  def step(self) -> None:
    # this is the function called by the controller
    raise NotImplementedError()


# Base classes, applicable generally

class OpenLink(Action):
  def __init__(self, text = "Open the following URL: {url}"):
    super().__init__(text=text)

  def step(self, driver):
    args = self.args

    # open this url
    driver.get(args["url"])


class TypeInput(Action):
  def __init__(self, text = "Type the following '{text}' in the input box"):
    super().__init__(text = text)

  def step(self, driver):
    args = self.args

    curr_url = driver.current_url
    if "google" in curr_url: # weird subroutine for google
      ele = driver.find_element_by_name("q")
    else:
      ele = driver.find_element_by_tag_name("input")
    ele.send_keys(args["text"])


class TypeInputAndPressEnter(Action):
  def __init__(self, text="Type the following '{text}' in the input box and press Enter"):
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


# class


# create a list that can be given to the user
DefaultActions = [
    OpenLink(),
    TypeInput(),
    TypeInputAndPressEnter()
]
