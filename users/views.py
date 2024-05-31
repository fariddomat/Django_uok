from django.shortcuts import render, redirect
from django.contrib.auth.backends import ModelBackend
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
from .models import Specification, Questionnaire, Prediction
from django.contrib.auth.decorators import login_required

# Load the trained model and preprocessing artifacts
model = joblib.load("random_forest_model.pkl")
onehot_encoder = joblib.load("onehot_encoder.pkl")
train_columns = joblib.load("train_columns.pkl")


@login_required
def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user

            # Save the questionnaire
            questionnaire = Questionnaire.objects.create(
                user=user,
                high_school_gpa=data['high_school_gpa_float'],
                region=data['region_str'],
                preferred_living=data['preferred_living_str'],
                choice_factors=data['choice_factors_str'],
                biggest_difficulty=data['biggest_difficulty_str'],
                preferred_subjects=", ".join(data['preferred_subjects_str']),
                disliked_subjects=", ".join(data['disliked_subjects_str']),
                university_type=data['university_type_str'],
                preferred_study_duration=data['preferred_study_duration_int']
            )

            # Prepare data for prediction
            input_data = {
                "high_school_gpa_float": data['high_school_gpa_float'],
                "region_str": data['region_str'],
                "preferred_living_str": data['preferred_living_str'],
                "choice_factors_str": data['choice_factors_str'],
                "biggest_difficulty_str": data['biggest_difficulty_str'],
                "preferred_subjects_str": ", ".join(data['preferred_subjects_str']),
                "disliked_subjects_str": ", ".join(data['disliked_subjects_str']),
                "university_type_str": data['university_type_str'],
                "preferred_study_duration_int": data['preferred_study_duration_int']
            }
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
            
            # Save the prediction
            prediction = Prediction.objects.create(
                user=user,
                questionnaire=questionnaire,
                recommended_branches=", ".join(top3_predictions[0])
            )


            return redirect('prediction_result_view', prediction_id=prediction.id)
    else:
        form = PredictionForm()

    return render(request, 'users/predict.html', {'form': form})

@login_required
def prediction_result_view(request, prediction_id):
    prediction = Prediction.objects.get(id=prediction_id, user=request.user)
    recommended_branches = prediction.recommended_branches.split(", ")
    print(recommended_branches)
    return render(request, 'users/predict_results.html', {'prediction': prediction, 'recommended_branches': recommended_branches})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Manually specifying the backend
            backend = 'django.contrib.auth.backends.ModelBackend'  # Use the correct backend here
            user.backend = backend
            login(request, user, backend=backend)
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
def manage_specifications(request):
    specifications = Specification.objects.all()
    return render(request, 'specifications/manage_specifications.html', {'specifications': specifications})

@user_passes_test(is_admin)
def create_specification(request):
    if request.method == 'POST':
        form = SpecificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_specifications')
    else:
        form = SpecificationForm()
    return render(request, 'specifications/specification_form.html', {'form': form, 'title': 'Create Specification'})

@user_passes_test(is_admin)
def update_specification(request, pk):
    specification = get_object_or_404(Specification, pk=pk)
    if request.method == 'POST':
        form = SpecificationForm(request.POST, instance=specification)
        if form.is_valid():
            form.save()
            return redirect('manage_specifications')
    else:
        form = SpecificationForm(instance=specification)
    return render(request, 'specifications/specification_form.html', {'form': form, 'title': 'Update Specification'})

@user_passes_test(is_admin)
def delete_specification(request, pk):
    specification = get_object_or_404(Specification, pk=pk)
    if request.method == 'POST':
        specification.delete()
        return redirect('manage_specifications')
    return render(request, 'specifications/specification_confirm_delete.html', {'specification': specification})