from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message
