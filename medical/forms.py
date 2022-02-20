from django import forms
from django.core import mail

import medical.models
import medical.widget


class MedicalForm(forms.models.BaseForm):
    template_name = 'base/medical_form.html'

    class Meta:
        pass


class VaccinationSubscribeForm(MedicalForm, forms.ModelForm):
    def after_save(self):
        mail.send_mail(
            '订阅成功',
            '你好， 您已订阅成功.',
            from_email='1134187280@qq.com', recipient_list=[
                self.cleaned_data['email_address']
            ])

    class Meta(MedicalForm.Meta):
        model = medical.models.VaccinationSubscribe
        fields = '__all__'
        widgets = {
            'related_vaccination': medical.widget.DisplayNoneWidget(),
            'subscribe_date_time': medical.widget.DisplayNoneWidget()
        }
