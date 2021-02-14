

class User:
  def __init__(self, token, secret, id, name):
    self.token = token
    self.secret = secret
    self.id = id
    self.name = name

  def dict(self):
    return {
      'token': self.token,
      'secret': self.secret,
      'id': self.id,
      'name': self.name
    }