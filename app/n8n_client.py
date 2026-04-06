import requests
from app.config import N8N_WEBHOOK_URL
from app.config import (N8N_EMAIL_WEBHOOK_URL)
from app.config import N8N_SIMPLIFY_WEBHOOK_URL
from fastapi import HTTPException

def send_to_n8n(contract_text: str):

    payload = {
        "contract_text": contract_text,
        "comparison": 0
    }

    print("\n Sending contract to n8n...")
    print("Webhook URL:", N8N_WEBHOOK_URL)

    response = requests.post(
        N8N_WEBHOOK_URL,
        json=payload,
        timeout=180
    )

    print("\n Response received from n8n")
    print("Status code:", response.status_code)

    data = response.json()

    print("\n AI RESPONSE:")
    print(data)

    return data

import requests
from app.config import N8N_WEBHOOK_URL


def send_comparison_to_n8n(contract1: str, contract2: str):

    payload = {

        "contract1": contract1,
        "contract2": contract2,
        "comparison": 1
    }

    print("\nSending contracts for comparison...")

    response = requests.post(

        N8N_WEBHOOK_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    print("\nComparison Result:")
    print(data)

    return data


def generate_negotiation_email(
    party_1: str,
    party_2: str,
    risky_clauses,
    key_concerns,
    improvement_recommendations = []
):


    payload = {

        "party_1": party_1,
        "party_2": party_2,

        "risky_clauses": risky_clauses,

        "key_concerns": key_concerns,

        "improvement_recommendations": improvement_recommendations
    }


    print("\nSending data to n8n email generator...")

    response = requests.post(

        N8N_EMAIL_WEBHOOK_URL,

        json = payload,

        timeout = 120
    )


    response.raise_for_status()

    data = response.json()


    print("\nGenerated Email:")
    print(data)


    return data


def send_simplification_to_n8n(contract_text: str):

    payload = {

        "contract_text": contract_text,

        "simplify": 1

    }

    print("\nSending contract for simplification...")

    response = requests.post(

        N8N_SIMPLIFY_WEBHOOK_URL,

        json = payload,

        timeout = 180

    )

    response.raise_for_status()

    data = response.json()

    print("\nSimplified contract response:")
    print(data)

    return data

def send_redraft_to_n8n(contract_text, clauses):

    url = "https://vanshkakkar.app.n8n.cloud/webhook/redraft-contract"

    payload = {

        "contract_text": contract_text,

        "clauses": clauses

    }

    response = requests.post(

        url,

        json = payload,

        timeout = 180

    )

    if response.status_code != 200:

        raise HTTPException(

            status_code = 500,

            detail = "n8n redraft workflow failed"

        )

    return response.content