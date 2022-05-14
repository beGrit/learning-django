from django import forms
from django.core import mail
from django.forms import HiddenInput, NumberInput
from django.template import Template, loader

import medical.models
import medical.widget


class VaccinationSubscribeForm(forms.ModelForm):

    def after_save(self):
        template: Template = loader.get_template('custom/emails/vaccination_subscribe.html')
        body_data = template.render(context={
            'data': self.cleaned_data
        })
        mail.send_mail(
            '订阅疫苗活动成功，请注意时间！！！',
            '',
            '1134187280@qq.com',
            recipient_list=[
                self.cleaned_data['email_address']
            ],
            html_message=body_data)

    class Meta:
        model = medical.models.VaccinationSubscribe
        fields = '__all__'
        widgets = {
            'related_vaccination': HiddenInput(),
            'birth': NumberInput(attrs={
                'type': 'date',
            }),
        }


class VolunteerRegisterForm(forms.ModelForm):
    class Meta:
        model = medical.models.Volunteer
        fields = [
            'name', 'gender', 'age', 'profile_picture',
            'work_date', 'is_student', 'no_salary', 'related_activity']
        widgets = {
            'work_date': NumberInput(attrs={
                'type': 'date',
            }),
        }
