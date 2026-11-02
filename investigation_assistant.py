from config.settings import get_settings
import json

def investigate(transaction, question):
    settings=get_settings()
    api_key=settings["openai_api_key"]
    if not api_key:
        return ("**Local investigation summary (OpenAI API not configured)**\n\n"
                f"- Transaction: `{transaction.get('transaction_id')}`\n"
                f"- Amount: `{transaction.get('amount')}`\n"
                f"- Frequency in 24h: `{transaction.get('frequency_24h')}`\n"
                f"- Account age (days): `{transaction.get('account_age_days')}`\n\n"
                "These are review indicators, not proof of fraud. Verify the transaction and supporting evidence.")
    try:
        from openai import OpenAI
        client=OpenAI(api_key=api_key)
        response=client.chat.completions.create(
            model=settings["openai_model"],
            messages=[
                {"role":"system","content":"You are a cautious payment-risk investigation assistant. Use only supplied facts. Never assert fraud as proven. Recommend human review."},
                {"role":"user","content":f"Transaction facts: {json.dumps(transaction,default=str)}\nQuestion: {question}"}
            ], temperature=.2)
        return response.choices[0].message.content
    except Exception as exc:
        return f"AI service unavailable: {exc}. Review the supplied transaction facts manually."
