from django import forms
from django.core import mail
from django.template import Template, loader

import medical.models
import medical.widget


class MedicalForm(forms.models.BaseForm):
    template_name = 'base/medical_form.html'

    class Meta:
        pass


class VaccinationSubscribeForm(MedicalForm, forms.ModelForm):
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

    class Meta(MedicalForm.Meta):
        model = medical.models.VaccinationSubscribe
        fields = '__all__'
        widgets = {
            'related_vaccination': medical.widget.DisplayNoneWidget(),
            'subscribe_date_time': medical.widget.DisplayNoneWidget()
        }
