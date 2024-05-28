from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .forms import PredictionForm
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import University, Specification
from .forms import UniversityForm, SpecificationForm

def predict(request):
    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data
            input_data['preferred_subjects_str'] = ', '.join(input_data['preferred_subjects_str'])
            input_data['disliked_subjects_str'] = ', '.join(input_data['disliked_subjects_str'])

            # Load the trained model and preprocessing artifacts
            model = joblib.load("random_forest_model.pkl")
            onehot_encoder = joblib.load("onehot_encoder.pkl")
            train_columns = joblib.load("train_columns.pkl")

            # Convert input data to DataFrame
            input_df = pd.DataFrame([input_data])

            # Apply one-hot encoding to categorical columns
            encoded_data = onehot_encoder.transform(input_df[['region_str', 'preferred_living_str', 'university_type_str']]).toarray()
            encoded_columns = onehot_encoder.get_feature_names_out(['region_str', 'preferred_living_str', 'university_type_str'])
            encoded_df = pd.DataFrame(encoded_data, columns=encoded_columns)
            input_df = input_df.join(encoded_df).drop(columns=['region_str', 'preferred_living_str', 'university_type_str'])

            # Convert multi-valued columns to one-hot encoding
            multi_valued_columns = ["preferred_subjects_str", "disliked_subjects_str", "choice_factors_str", "biggest_difficulty_str"]
            for column in multi_valued_columns:
                dummies = input_df[column].str.get_dummies(sep=", ")
                dummies.columns = [f"{col}_{column}" for col in dummies.columns]
                input_df = input_df.join(dummies).drop(column, axis=1)

            # Fill missing columns to match the training set
            missing_cols = set(train_columns) - set(input_df.columns)
            for c in missing_cols:
                input_df[c] = 0

            # Ensure correct column order
            input_df = input_df[train_columns]

            # Predict probabilities with the trained model
            prediction_proba = model.predict_proba(input_df)

            # Get the top three most likely classes (interested branches)
            top3_indices = np.argsort(prediction_proba, axis=1)[:, -3:]
            top3_predictions = [[model.classes_[i] for i in row] for row in top3_indices]

            # Logical constraints for preferred subjects based on interested branches
            preferred_subjects_mapping = {
                "علوم الكمبيوتر": ["التكنولوجيا والحاسوب", "الرياضيات", "اللغة الانكليزية"],
                "هندسة البرمجيات": ["التكنولوجيا والحاسوب", "الرياضيات"],
                "الطب البشري": ["علم الأحياء", "الكيمياء"],
                "طب الأسنان": ["علم الأحياء", "الكيمياء"],
                "الصيدلة": ["علم الأحياء", "الكيمياء"],
                "الهندسة المعمارية": ["الرياضيات", "الفيزياء"],
                "الهندسة المدنية": ["الرياضيات", "الفيزياء"],
                "هندسة التحكم الآلي": ["الرياضيات", "الفيزياء"],
                "الأداب": ["اللغة العربية", "اللغة الانكليزية", "العلوم الاجتماعية"],
                "الحقوق": ["العلوم الاجتماعية", "اللغة العربية"],
                "العلوم الطبيعية": ["علم الأحياء", "الكيمياء", "الفيزياء"],
                "رياض الأطفال": ["العلوم الاجتماعية", "التربية"],
                "التربية": ["العلوم الاجتماعية", "التربية"],
                "الرياضيات": ["الرياضيات"],
                "الفيزياء": ["الفيزياء"],
                "الكيمياء": ["الكيمياء"],
                "الموسيقى": ["الفنون", "الثقافة"]
            }

            # Get the disliked subjects
            disliked_subjects = input_data["disliked_subjects_str"].split(", ")

            # Filter predictions based on logical constraints
            filtered_predictions = []
            for branch in top3_predictions[0]:
                preferred_subjects = preferred_subjects_mapping.get(branch, [])
                if not any(disliked in preferred_subjects for disliked in disliked_subjects):
                    filtered_predictions.append(branch)

            # If less than 3 predictions remain, add more from the sorted list
            if len(filtered_predictions) < 3:
                sorted_predictions = [model.classes_[i] for i in np.argsort(prediction_proba, axis=1)[0][::-1]]
                for pred in sorted_predictions:
                    preferred_subjects = preferred_subjects_mapping.get(pred, [])
                    if pred not in filtered_predictions and not any(disliked in preferred_subjects for disliked in disliked_subjects):
                        filtered_predictions.append(pred)
                    if len(filtered_predictions) == 3:
                        break

            # Output the top three predictions
            context = {
                "form": form,
                "predictions": filtered_predictions[:3]
            }
            return render(request, "users/predict_results.html", context)
    else:
        form = PredictionForm()
    return render(request, "users/predict.html", {"form": form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def home(request):
    return render(request, 'users/home.html')



def is_admin(user):
    return user.is_authenticated and user.is_admin


@user_passes_test(is_admin)
def manage_universities(request):
    universities = University.objects.all()
    return render(request, 'universities/manage_universities.html', {'universities': universities})

@user_passes_test(is_admin)
def create_university(request):
    if request.method == 'POST':
        form = UniversityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_universities')
    else:
        form = UniversityForm()
    return render(request, 'universities/university_form.html', {'form': form, 'title': 'Create University'})

@user_passes_test(is_admin)
def update_university(request, pk):
    university = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        form = UniversityForm(request.POST, instance=university)
        if form.is_valid():
            form.save()
            return redirect('manage_universities')
    else:
        form = UniversityForm(instance=university)
    return render(request, 'universities/university_form.html', {'form': form, 'title': 'Update University'})

@user_passes_test(is_admin)
def delete_university(request, pk):
    university = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        university.delete()
        return redirect('manage_universities')
    return render(request, 'universities/confirm_delete.html', {'object': university})

@user_passes_test(is_admin)
def specification_list(request):
    specifications = Specification.objects.all()
    return render(request, 'specifications/specification_list.html', {'specifications': specifications})

@user_passes_test(is_admin)
def specification_create(request):
    if request.method == "POST":
        form = SpecificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('specification_list')
    else:
        form = SpecificationForm()
    return render(request, 'specifications/specification_form.html', {'form': form})

@user_passes_test(is_admin)
def specification_update(request, pk):
    specification = get_object_or_404(Specification, pk=pk)
    if request.method == "POST":
        form = SpecificationForm(request.POST, instance=specification)
        if form.is_valid():
            form.save()
            return redirect('specification_list')
    else:
        form = SpecificationForm(instance=specification)
    return render(request, 'specifications/specification_form.html', {'form': form})

@user_passes_test(is_admin)
def specification_delete(request, pk):
    specification = get_object_or_404(Specification, pk=pk)
    if request.method == "POST":
        specification.delete()
        return redirect('specification_list')
    return render(request, 'specifications/specification_confirm_delete.html', {'specification': specification})