from wtforms import Form

from utils import log


class BaseForm(Form):
    def get_error(self):
        # log("self.errors: ", self.errors)
        message = self.errors.popitem()[1][0]
        return message
