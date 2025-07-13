from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth import authenticate, login
import re
from django.http import JsonResponse
from meilisearch import Client
import os


import re

def api_search(request):
    import re
    from meilisearch import Client
    import os
    from django.http import JsonResponse

    query = request.GET.get('q', '').strip()
    print("recherche globale")
    client = Client(os.getenv("MEILI_URL"))

    search_term = query.lstrip('=').lower()

    indexes = {
        'moniteur': 'moniteur_docs',
        'eurlex': 'eurlex_docs',
        'CEtat': 'conseil_etat_arrets100',
        'CA': 'constcourtjudgments2025',
        'Annexe': 'annexes_juridique',
        'Projet': 'propositions_et_loisbisbis'
    }

    results = {}

    for key, index_name in indexes.items():
        try:
            raw_hits = client.index(index_name).search(search_term).get('hits', [])
        except Exception as e:
            print(f"[ERREUR] Index '{key}' → {e}")
            raw_hits = []

        filtered_hits = [
            hit for hit in raw_hits
            if re.search(
                rf'\b{re.escape(search_term)}\b',
                (
                    str(hit.get("text") or "") +
                    str(hit.get("pdf_text") or "") +
                    str(hit.get("contenu") or "") +
                    str(hit.get("texte") or "")
                ),
                re.IGNORECASE
            )
        ]

        results[key] = filtered_hits

    return JsonResponse(results)

def api_search_niss(request):
    query = request.GET.get('q', '').strip()
    print(f"NISS query: {query}")
    client = Client(os.getenv("MEILI_URL"))
    # Ne modifie pas la structure
    search_term = query  # Pas de transformation ici

    indexes = {
        'moniteur': 'moniteur_docs',
        'eurlex': 'eurlex_docs',
        'CEtat': 'conseil_etat_arrets100',
        'CA': 'constcourtjudgments2025',
        'Annexe': 'annexes_juridique'
    }

    results = {}

    for key, index_name in indexes.items():
        try:
            raw_hits = client.index(index_name).search(search_term).get('hits', [])
        except Exception as e:
            print(f"[ERREUR] Index '{key}' → {e}")
            raw_hits = []

        # Match textuellement
        filtered_hits = [
            hit for hit in raw_hits
            if search_term in hit.get("text", "")
        ]

        results[key] = filtered_hits

    return JsonResponse(results)



def api_search_tva(request):
    query = request.GET.get('q', '').strip()
    print(f"TVA query: {query}")
    client = Client(os.getenv("MEILI_URL"))

    search_term = query.lstrip('=').lower()

    indexes = {
        'moniteur': 'moniteur_docs',
        'eurlex': 'eurlex_docs',
        'CEtat': 'conseil_etat_arrets100',
        'CA': 'constcourtjudgments2025',
        'Annexe': 'annexes_juridique'
    }

    results = {}

    for key, index_name in indexes.items():
        try:
            raw_hits = client.index(index_name).search(search_term).get('hits', [])
        except Exception as e:
            print(f"[ERREUR] Index '{key}' → {e}")
            raw_hits = []

        filtered_hits = [
            hit for hit in raw_hits
            if search_term in hit.get("text", "").lower()
        ]

        results[key] = filtered_hits

    return JsonResponse(results)


def home(request):
    return render(request, 'veille/home.html')

def charts(request):
    return render(request, 'veille/charts.html')

def contact(request):
    return render(request, 'veille/contact.html')

def fonctionnalites(request):
    return render(request, 'veille/fonctionnalites.html')

def recherches(request):
    return render(request, 'veille/recherches.html')

def resultats(request):
    return render(request, 'veille/resultats.html')

def maveille(request):
    return render(request, 'veille/maveille.html')

def premium(request):
    return render(request, 'veille/premium.html')






def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        username = email  # Ici, on prend l'email comme username

        # Vérifie mot de passe identique
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "veille/register.html")

        # Vérifie si le compte existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Un compte avec cet email existe déjà.")
            return render(request, "veille/register.html")

        # Crée le User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Crée le UserProfile
        UserProfile.objects.create(user=user)

        messages.success(request, "Votre compte a été créé. Vous pouvez vous connecter.")
        return redirect("login")

    return render(request, "veille/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Rappel: on utilise l'email comme username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # À remplacer par le nom de ton URL d'accueil
        else:
            messages.error(request, "Email ou mot de passe invalide.")
    return render(request, "veille/login.html")
