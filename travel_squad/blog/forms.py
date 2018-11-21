from django import forms


class SearchForm(forms.Form):
	query = forms.CharField(label='',required=False, max_length=1000,
									widget=forms.TextInput(attrs={
											'placeholder': 'Search',
											'class': 'form-control mr-sm-2',
											'aria-label': 'Search',
											'id': 'inputed_query'
										}
									)
								)
