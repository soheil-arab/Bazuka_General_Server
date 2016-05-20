from django.test import TestCase

# Create your tests here.
import Crypto
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from datetime import datetime



msg = datetime.now().__str__()
file = open('public.pem', 'r')
pk = RSA.importKey(file.read())
file = open('private.pem', 'r')
sk = RSA.importKey(file.read())
signer = PKCS1_v1_5.new(sk)
h = SHA256.new(msg.encode())
signature = signer.sign(h)
verifier = PKCS1_v1_5.new(pk)
h = SHA256.new(msg.encode())
if verifier.verify(h, signature):
    print('yes')
else:
    print('no')