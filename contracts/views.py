from docusign_esign import EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients, ApiClient
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from docusign_esign.client.api_exception import ApiException
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from core import settings
import requests
import base64

from docusign_esign.models import RecipientViewRequest
from .forms import RegisterForm, ContractForm
from .docusign_auth import get_access_token
from .models import Contract
import urllib.parse


@login_required
def home(request):
    return render(request, 'contracts/home.html')

# Register view 
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            contract = Contract(user=user, contract_text="contract text")
            contract.save()
            return redirect('home')

    else:
        form = RegisterForm()
    return render(request, 'contracts/register.html', {'form': form})


@login_required
def create_contract(request):
    if request.method == 'POST':
        contract_text = request.POST.get('contract_text', '')
        other_signer_name = request.POST.get('other_signer_name', '')  
        other_signer_email = request.POST.get('other_signer_email', '')

        contract = Contract(
            user = request.user,
            contract_text = contract_text,
            email_of_other_signer = other_signer_email,
            name_of_other_signer = other_signer_name  
        )
        contract.save()
        return redirect('redirect_to_docusign')
    return render(request, 'contracts/create_contract.html')

def redirect_to_docusign(request):
    contract = Contract.objects.filter(user=request.user).last()
    document_content = contract.contract_text
    signer_name = contract.name_of_other_signer
    signer_email = contract.email_of_other_signer

    auth_url = (
        f"{settings.DOCUSIGN_AUTH_SERVER}/oauth/auth"
        f"?response_type=code"
        f"&scope=signature"
        f"&client_id={settings.DOCUSIGN_CLIENT_ID}"
        f"&redirect_uri={settings.DOCUSIGN_REDIRECT_URI}"
        f"&contract_text={document_content}"
        f"&signer_name={signer_name}"  
        f"&signer_email={signer_email}"  
    )

    auth_url = auth_url.replace('account.docusign.com', 'account-d.docusign.com')
    return redirect(auth_url)


def docusign_callback(request):
    authorization_code = request.GET.get("code")
    if not authorization_code:
        return HttpResponse("Error: Authorization code not provided.", status=400)

    url = f"{settings.DOCUSIGN_AUTH_SERVER}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": settings.DOCUSIGN_REDIRECT_URI,
        "client_id": settings.DOCUSIGN_CLIENT_ID,
        "client_secret": settings.DOCUSIGN_CLIENT_SECRET,
    }

    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    if response.status_code == 200:
        access_token = response_data["access_token"]
        request.user.docusign_access_token = access_token
        request.user.save()

        request.session["docusign_access_token"] = access_token
        return redirect('contracts_overview') 
    else:
        return HttpResponse(f"Error obtaining access token: {response_data}", status=400)

@login_required
def start_signing(request, contract):
    access_token = request.session.get("docusign_access_token")
    if not access_token:
        return redirect('docusign_login')

    signer_email = contract.email_of_other_signer
    signer_name = contract.name_of_other_signer
    document_content = contract.contract_text

    envelope_url = f"{settings.DOCUSIGN_API_BASE_URL}/v2.1/accounts/{settings.DOCUSIGN_ACCOUNT_ID}/envelopes"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    envelope_definition = {
        "emailSubject": "Please sign this contract.",
        "status": "sent",
        "documents": [
            {
                "documentBase64": base64.b64encode(document_content.encode("utf-8")).decode("utf-8"),
                "name": "Contract Document",
                "fileExtension": "txt",
                "documentId": "1"
            }
        ],
        "recipients": {
            "signers": [
                {
                    "email": signer_email,
                    "name": signer_name,
                    "recipientId": "2",
                    "routingOrder": "1"
                }
            ]
        }
    }

    response = requests.post(envelope_url, headers=headers, json=envelope_definition)
    if response.status_code == 201:
        envelope_id = response.json()["envelopeId"]
        contract.envelope_id = envelope_id
        contract.save()

        messages.success(request, 'The contract has been sent for signing.')
        return redirect('contracts_detail', contract_id=contract.id)

    else:
        return HttpResponse(f"Error creating envelope: {response.json()}", status=400)


# Check contract status view
@login_required
def check_contract_status(request, contract):
    access_token = request.session.get("docusign_access_token")
    if not access_token:
        return redirect('docusign_login')

    try:
        headers = {"authorization": f"Bearer {access_token}"}
        url = f"https://demo.docusign.net/restapi/v2.1/accounts/{settings.DOCUSIGN_ACCOUNT_ID}/envelopes/{contract.envelope_id}"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            envelope_status = response.json()["status"]
            if envelope_status == "completed" and not contract.is_signed:
                contract.is_signed = True
                contract.last_status_update = timezone.now()
                contract.save()
                send_confirmation_email(request.user.email, contract.id)
                message = "the contract has signed by both sides"
            else:
                message = "the contract has not been fully signed yet."
        else:
            message = f"Error fetching envelope status: {response.json()}"
    except Exception as e:
        message = f"an error occured while fetching the contract status {str(e)}"
    
    return render(request, 'contracts/contract_status.html', {
        'message': message,
        'last_update': contract.last_status_update
    })

# Send confirmation email
def send_confirmation_email(user_email, contract_id):
    subject = "contract signing completed"
    message = f"your contract with id{contract_id} it has been signed by both parties."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])

@login_required
def contracts_overview(request):
    contracts = Contract.objects.all()  
    return render(request, 'contracts/contract_detail.html', {'contracts': contracts})
