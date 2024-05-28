from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_user', 'is_admin')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PredictionForm(forms.Form):
    HIGH_SCHOOL_GPA_CHOICES = [(i, i) for i in range(60, 101)]
    REGION_CHOICES = [
        ("دمشق", "دمشق"),
        ("ريف دمشق", "ريف دمشق"),
        ("حلب", "حلب"),
        ("حمص", "حمص"),
        ("حماة", "حماة"),
        ("اللاذقية", "اللاذقية"),
        ("طرطوس", "طرطوس"),
        ("إدلب", "إدلب"),
        ("درعا", "درعا"),
        ("السويداء", "السويداء"),
        ("القنيطرة", "القنيطرة"),
        ("دير الزور", "دير الزور"),
        ("الرقة", "الرقة"),
        ("الحسكة", "الحسكة"),
    ]
    LIVING_CHOICES = [
        ("مدينة قريبة", "مدينة قريبة"),
        ("السفر يوميًا", "السفر يوميًا"),
        ("لا فرق", "لا فرق"),
    ]
    CHOICE_FACTORS_CHOICES = [
        ("المعدل الجامعي", "المعدل الجامعي"),
        ("الشغف والطموح", "الشغف والطموح"),
        ("الفرص الوظيفية", "الفرص الوظيفية"),
        ("الدخل المتوقع", "الدخل المتوقع"),
        ("الرغبة العائلية", "الرغبة العائلية"),
        ("الرغبة الاجتماعية", "الرغبة الاجتماعية"),
        ("السمعة الأكاديمية", "السمعة الأكاديمية"),
        ("الاهتمامات الشخصية", "الاهتمامات الشخصية"),
        ("الصعوبة الدراسية", "الصعوبة الدراسية"),
        ("العلاقات الإنسانية", "العلاقات الإنسانية"),
    ]
    DIFFICULTY_CHOICES = [
        ("عدم معرفة ما أريد", "عدم معرفة ما أريد"),
        ("عدم معرفة ما هي الفروع المتاحة", "عدم معرفة ما هي الفروع المتاحة"),
        ("عدم معرفة ما هي متطلبات الفروع", "عدم معرفة ما هي متطلبات الفروع"),
        ("عدم معرفة ما هي مزايا وعيوب الفروع", "عدم معرفة ما هي مزايا وعيوب الفروع"),
        ("عدم معرفة ما هي آراء الآخرين عن الفروع", "عدم معرفة ما هي آراء الآخرين عن الفروع"),
        ("عدم معرفة ما هي توقعات السوق عن الفروع", "عدم معرفة ما هي توقعات السوق عن الفروع"),
        ("عدم وجود مصادر موثوقة للمعلومات", "عدم وجود مصادر موثوقة للمعلومات"),
        ("عدم وجود مشورة مهنية", "عدم وجود مشورة مهنية"),
        ("عدم وجود دعم نفسي", "عدم وجود دعم نفسي"),
        ("عدم وجود دعم مادي", "عدم وجود دعم مادي"),
    ]
    SUBJECT_CHOICES = [
        ("علم الأحياء", "علم الأحياء"),
        ("الكيمياء", "الكيمياء"),
        ("الرياضيات", "الرياضيات"),
        ("الفيزياء", "الفيزياء"),
        ("اللغة العربية", "اللغة العربية"),
        ("اللغة الانكليزية", "اللغة الانكليزية"),
        ("اللغة الفرنسية", "اللغة الفرنسية"),
        ("العلوم الاجتماعية والإنسانية", "العلوم الاجتماعية والإنسانية"),
        ("التاريخ", "التاريخ"),
        ("الجغرافيا", "الجغرافيا"),
        ("الفلسفة", "الفلسفة"),
        ("التكنولوجيا والحاسوب", "التكنولوجيا والحاسوب"),
        ("الفنون", "الفنون"),
        ("الثقافة", "الثقافة"),
        ("غير ذلك", "غير ذلك"),
    ]
    UNIVERSITY_TYPE_CHOICES = [
        ("حكومية", "حكومية"),
        ("خاصة", "خاصة"),
    ]
    STUDY_DURATION_CHOICES = [(i, i) for i in range(4, 7)]

    high_school_gpa_float = forms.ChoiceField(choices=HIGH_SCHOOL_GPA_CHOICES, label="المعدل الثانوي", widget=forms.Select(attrs={'class': 'form-control'}))
    region_str = forms.ChoiceField(choices=REGION_CHOICES, label="المنطقة", widget=forms.Select(attrs={'class': 'form-control'}))
    preferred_living_str = forms.ChoiceField(choices=LIVING_CHOICES, label="السكن المفضل", widget=forms.Select(attrs={'class': 'form-control'}))
    choice_factors_str = forms.ChoiceField(choices=CHOICE_FACTORS_CHOICES, label="عوامل الاختيار", widget=forms.Select(attrs={'class': 'form-control'}))
    biggest_difficulty_str = forms.ChoiceField(choices=DIFFICULTY_CHOICES, label="أكبر الصعوبات", widget=forms.Select(attrs={'class': 'form-control'}))
    preferred_subjects_str = forms.MultipleChoiceField(choices=SUBJECT_CHOICES, label="المواد المفضلة", widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    disliked_subjects_str = forms.MultipleChoiceField(choices=SUBJECT_CHOICES, label="المواد غير المفضلة", widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}))
    university_type_str = forms.ChoiceField(choices=UNIVERSITY_TYPE_CHOICES, label="نوع الجامعة", widget=forms.Select(attrs={'class': 'form-control'}))
    preferred_study_duration_int = forms.ChoiceField(choices=STUDY_DURATION_CHOICES, label="مدة الدراسة المفضلة", widget=forms.Select(attrs={'class': 'form-control'}))