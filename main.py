from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from dotenv import load_dotenv
import os
import smtplib

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('APP.SECRET_KEY')

my_email = os.getenv('MY_EMAIL')
email_password = os.getenv('EMAIL_PASSWORD')
target_email = os.getenv('TARGET_EMAIL')


#   Test Enviroment variables
# print('PATH', os.getenv('PATH'))


class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    phone = IntegerField(label='Phone', validators=[DataRequired()])
    message = TextAreaField(label='Message', validators=[DataRequired(), Length(max=120)])

    submit = SubmitField(label='submit')


def send_email(name, email, phone, message):
    email_message = f"Subject:Portfolio Message ALERT!!\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
        # tls creates a secure connection
        connection.starttls()
        # login using the username and password
        connection.login(user=my_email, password=email_password)
        # specify the address you will use and message
        connection.sendmail(
            from_addr=my_email,
            to_addrs=target_email,
            # format for email
            msg=email_message)


@app.route("/", methods=['GET', 'POST'])
def home():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        name = contact_form.name.data
        email = contact_form.email.data
        phone = contact_form.phone.data
        message = contact_form.message.data
        send_email(name, email, phone, message)
        return render_template('index.html', form=contact_form, msg_sent=True)
    else:
        return render_template("index.html", form=contact_form, msg_sent=False)


if __name__ == '__main__':
    app.run()
