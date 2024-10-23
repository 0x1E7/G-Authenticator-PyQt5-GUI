import hmac, base64, struct, hashlib, time
import pickle

secrets_file = "secrets.pkl"

def get_hotp_token(secret, intervals_no):
	"""This is where the magic happens."""
	key = base64.b32decode(normalize(secret), True) # True is to fold lower into uppercase
	msg = struct.pack(">Q", intervals_no)
	h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
	o = h[19] & 15
	h = str((struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000)
	return prefix0(h)

def get_totp_token(secret):
	"""The TOTP token is just a HOTP token seeded with every 30 seconds."""
	return get_hotp_token(secret, intervals_no=int(time.time())//30)

def normalize(key):
	"""Normalizes secret by removing spaces and padding with = to a multiple of 8"""
	k2 = key.strip().replace(' ','')
	# k2 = k2.upper()	# skipped b/c b32decode has a foldcase argument
	if len(k2)%8 != 0:
		k2 += '='*(8-len(k2)%8)
	return k2

def prefix0(h):
	"""Prefixes code with leading zeros if missing."""
	if len(h) < 6:
		h = '0'*(6-len(h)) + h
	return h

def ACCOUNT_ADD(name: str, secret: str) -> None:
	try:
		with open(secrets_file, "rb") as f:
			loaded_dict = pickle.load(f)
	except:
		with open(secrets_file, "xb") as f:
			loaded_dict = {}
			pickle.dump(loaded_dict, f)
	loaded_dict[name] = secret
	with open(secrets_file, "wb") as f:
		pickle.dump(loaded_dict, f)

def ACCOUNT_REMOVE(name: str) -> None:
	with open(secrets_file, "rb") as f:
		loaded_dict = pickle.load(f)
		del loaded_dict[name]
	with open(secrets_file, "wb") as f:
		pickle.dump(loaded_dict, f)

def SHOW_ALL_CODES() -> dict | None:
	try:
		with open(secrets_file, "rb") as f:
			loaded_dict = pickle.load(f)
		return loaded_dict
	except:
		return None

if __name__ == "__main__":
	#ACCOUNT_ADD("John", "6HLV Z46X TNV2 NXGT")
	SHOW_ALL_CODES()
