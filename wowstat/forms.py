# -*- coding: utf-8 -*-

from django import forms

class DateChoices(forms.Form):
	"""
	Form for choice of date to outpute log from wowza.
	"""
	date_choice = forms.DateField(help_text=u"Форматы: '2006-10-25', '10/25/2006', '10/25/06'", 
	                              widget=forms.TextInput(attrs={'style':'width:6em'}))