from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


"""
class RegistrationForm(FlaskForm):
	username = StringField('username',
                           validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
                        validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])
	password_confirm = PasswordField('password_confirm',
                                     validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')
	def validate_username(self, username):
		user = users.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')
	def validate_email(self, email):
		user = users.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one.')
"""
class RegistrationForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired(), Email()])
	password_confirmation = PasswordField('password_confirmation', validators=[DataRequired(), EqualTo('password')])
	"""def validate_username(self, username):
		user = db.execute('SELECT username FROM users').fetchall()
		for u in user :
			if u == username:
				raise ValidationError('That email is taken. Please choose a different one.')
"""
class LogInForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class searchForm(FlaskForm):
	bbar = StringField('search_bar', validators=[DataRequired()])

class reviewsForm(FlaskForm):
	comment = StringField('comment', validators=[Length(max=50)])
