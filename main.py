from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
app.secret_key = 'a random string'


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    phone = IntegerField(label='Phone', validators=[DataRequired()])
    message = TextAreaField(label='Message', validators=[DataRequired()])
    submit = SubmitField(label='submit')


@app.route("/", methods=['GET', 'POST'])
def home():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        name = contact_form.name.data
        email = contact_form.email.data
        phone = contact_form.phone.data
        message = contact_form.message.data
        print(name, email, phone, message)
        return render_template('index.html', form=contact_form, msg_sent=True, )
    else:

        return render_template("index.html", form=contact_form, msg_sent=False)




if __name__ == '__main__':
    app.run()