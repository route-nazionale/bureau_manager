#!/usr/bin/env python

from django.conf import settings

from Crypto.Cipher import AES
import base64
import os

BLOCK_SIZE = 32

def pkcs5_pad(blockSize,s):
	"""
	padding to blocksize according to PKCS #5
	calculates the number of missing chars to BLOCK_SIZE and pads with
	ord(number of missing chars)
	@see: http://www.di-mgt.com.au/cryptopad.html


	@param s: string to pad
	@type s: string

	@rtype: string
	"""
	return s + (blockSize - len(s) % blockSize) * chr(blockSize - len(s) % blockSize)

# the block size for the cipher object; must be 16, 24, or 32 for AES
# BLOCK_SIZE = 32

def get_crypto_base64_rn2014(message):

    # AAA: get keys from database "config" ?!?

    # 32
    KEY = base64.b64decode(settings.CRYPTO_KEY)

    # 16
    IV = base64.b64decode(settings.CRYPTO_KEY_IV)

    # END AAA

    obj = AES.new(KEY, AES.MODE_CBC, IV)
    ciphertext = obj.encrypt(pkcs5_pad(BLOCK_SIZE,message))
    return base64.b64encode(ciphertext)
