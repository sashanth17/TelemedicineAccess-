import requests
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)


# Twilio
ACCOUNT_SID = "AC0cc9356b15491a0aea1841d5b200c236"
AUTH_TOKEN = "e9d6552b972d659d4233acfcd1a16cf2"


@app.route("/voice", methods=["POST"])
def voice():
    """
    Entry point when Twilio receives a call.
    Greets the caller and asks for input.
    """
    resp = VoiceResponse()
    gather = resp.gather(
        input="speech",
        action="/gather",
        method="POST",
        timeout=5
    )
    gather.say("Hello! You are connected to the sashanth's telemedicine assistant. Please describe your symptoms after the beep.")
    resp.redirect("/voice")  # If no input, loop back
    return Response(str(resp), mimetype="application/xml")


# @app.route("/gather", methods=["POST"])
# def gather():
#     """
#     Handles captured speech from the caller.
#     Sends transcription to Gemini and speaks back the result.
#     """
#     user_input = request.form.get("SpeechResult", "No speech detected")
#     print(f"[DEBUG] Caller said: {user_input}")

#     # Call Gemini API
#     headers = {"Content-Type": "application/json"}
#     payload = {"contents": [{"parts": [{"text": user_input}]}]}

#     try:
#         gemini_resp = requests.post(
#             f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
#             headers=headers,
#             json=payload,
#             timeout=10
#         ).json()

#         gemini_text = gemini_resp["candidates"][0]["content"]["parts"][0]["text"]
#     except Exception as e:
#         print("[ERROR] Gemini API:", e)
#         gemini_text = "Sorry, I could not process your request right now."

#     print(f"[DEBUG] Gemini response: {gemini_text}")

#     # Speak Gemini's reply back
#     resp = VoiceResponse()
#     resp.say(gemini_text)
#     resp.redirect("/voice")  # Loop for next question
#     return Response(str(resp), mimetype="application/xml")
@app.route("/gather", methods=["POST"])
def gather():
    user_input = request.form.get("SpeechResult", "No speech detected")
    print(f"[DEBUG] Caller said: {user_input}")

    # Default fallback message
    gemini_text = "Sorry, the assistant is unavailable right now."

    try:
        # Call your AI Server instead of Gemini directly
        ai_resp = requests.post(
            "https://ai-server-p4fk.onrender.com/prompt", 
            json={"query": user_input},
            timeout=8
        ).json()

        gemini_text = ai_resp.get("answer", gemini_text)

    except Exception as e:
        print("[ERROR] AI Server call failed:", e)

    # Always return valid TwiML to Twilio
    resp = VoiceResponse()
    resp.say(gemini_text)
    resp.redirect("/voice")  # loop for next question
    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)