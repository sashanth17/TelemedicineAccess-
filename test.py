from twilio.rest import Client

account_sid = "AC0cc9356b15491a0aea1841d5b200c236"
auth_token = "e9d6552b972d659d4233acfcd1a16cf2"

client = Client(account_sid, auth_token)

call = client.calls.create(
    to="+917558187099",  # your verified number
    from_="+14127252099",  # your Twilio trial number
    url="https://telemedicineaccess.onrender.com/voice"
)

print("Call SID:", call.sid)
