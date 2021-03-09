import hashlib

def gather_all_attributes_for_element(driver, element):
  """function to capture all the attributes of any element.
  https://stackoverflow.com/questions/27307131/selenium-webdriver-how-do-i-find-all-of-an-elements-attributes
  """
  return driver.execute_script(
    '''
    var items = {};
    for (index = 0; index < arguments[0].attributes.length; ++index) {
      items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value
    };
    return items;
    ''',
    element
  )


class IgymElement():
  # our Wrapper for keeping all the information for that web element
  def __init__(self, **kwargs):
    self._args = []
    for k,v in kwargs.items():
      setattr(self, k, v)
      self._args.append(k)

  def __getitem__(self, name: str):
      return getattr(self, name)

  def _hash(self):
    data_str = " ".join([f"{k}={getattr(self, k)}" for k in self._args])
    return hashlib.md5(data_str.encode("utf-8")).hexdigest()
