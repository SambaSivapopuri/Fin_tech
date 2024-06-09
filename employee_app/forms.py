from django import forms

class AddressForm(forms.Form):
    hno = forms.CharField(max_length=255)
    street = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    state = forms.CharField(max_length=255)

class WorkExperienceForm(forms.Form):
    companyName = forms.CharField(max_length=255)
    fromDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    toDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(max_length=255)

class QualificationForm(forms.Form):
    qualificationName = forms.CharField(max_length=255)
    percentage = forms.FloatField()

class ProjectForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    photo = forms.CharField(widget=forms.Textarea)  # Base64 image data

class EmployeeForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    age = forms.IntegerField()
    gender = forms.CharField(max_length=10)
    phoneNo = forms.CharField(max_length=15)
    addressDetails = AddressForm()
    workExperience = WorkExperienceForm()
    qualifications = QualificationForm()
    projects = ProjectForm()
