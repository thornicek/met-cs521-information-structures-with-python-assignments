# Tomas Hornicek, no collaborators, no sources, no extension
import binascii
import csv
import random
from base64 import b64encode

'''
A Set of helper functions.

'''

def binary_to_string(n):
	# Helper function that will return ascii from binary
	# Use this to get the original message from a binary number
	return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()


def string_to_binary(string):
	# Helper function that will return binary from string
	# Use this to get a number from the message
	return int.from_bytes(string.encode(), 'big')


def binary_to_binary_string(binary):
	# Helper function that will return binary as a bit string from binary
	# Use this to convert the binary number into a string of 0s and 1s.
	# This is needed to generate the appropriate random key
	return bin(binary)[2:]


def binary_string_to_binary(bin_string):
	# Helper function that will return binary from a bit string
	# Use this to convert the random key into a number for calculations
	return int(bin_string, 2)


def get_random_bit():
	# Helper function that will randomly return either 1 or 0 as a string
	# Use this to help generate the random key for the OTP
	return str(random.randint(0, 1))


def read_message():
	# Helper function that will read and process message.txt which will provide a good tessting message
	message = ''
	f = open('message.txt', 'r')
	for line in f:
		message += line.replace('\n', ' ').lower()
	return message


class Cipher:

	def __init__(self):
		# Initialize the suite
		# In part 1 create letter_dict and inverse_dict
		# In part 3 create letter_heuristics and call self.read_csv()
		self.letter_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
							'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,
							'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20,
							'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, ' ': 26}
		self.inverse_dict = {v: k for k, v in self.letter_dict.items()}
		self.letter_heuristics = {}
		# self.wordlist = []
		self.read_csv()

	def rotate_letter(self, letter, n):
		# Rotate a letter by n and return the new letter
		corespond_num = self.letter_dict[letter]
		# Shift letter by n and use modulo to wrap around back to index 0, when 26 exceeded
		letter_shift = (corespond_num + n) % 27
		rotated = self.inverse_dict[letter_shift]
		return rotated

	def encode_caesar(self, message, n):
		# Encode message using rotate_letter on every letter and return the cipher text
		# Convert message to list, as strings are immutable
		message = list(message)
		# Iterate over message and rotate each letter by n
		for index, char in enumerate(message):
			message[index] = self.rotate_letter(char,n)
		# Convert from list of char to string
		message = ''.join(message)
		return message

	def decode_caesar(self, cipher_text, n):
		# Decode a cipher text by using rotate_letter the opposite direction and return the original message
		cipher_text = list(cipher_text)
		# Iterate over encrypted message and rotate each letter by -n
		for index, char in enumerate(cipher_text):
			cipher_text[index] = self.rotate_letter(char, -n)
		cipher_text = ''.join(cipher_text)
		return cipher_text



	def read_csv(self):
		# Read the letter frequency csv and create a heuristic save in a class variable
		file = 'letter_frequencies.csv'
		# Open csv file, using context manager, and read it
		with open(file,mode="r", encoding='utf-8-sig') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			# Iterate through the csv file, cast all letters to lowercase, and cast 2nd column to float
			for row in csv_reader:
				self.letter_heuristics[row['Letter'].lower()] = float(row['COUNT (In Billions)'])


	def score_string(self, string):
		# Score every letter of a string and return the total
		total = 0
		for char in string:
			total += self.letter_heuristics[char]
		return total

	def crack_caesar(self, cipher_text):
		# Break a caesar cipher by finding and returning the most probable outcome
		totals = dict()
		# Iterate through the possible shifts and add together the total of each shift
		for n in range(0,27):
			totals[n] = self.score_string(self.encode_caesar(cipher_text,n))
		# Find the maximum total and return it
		max_totals = max(totals, key = totals.get)
		clear_text = self.encode_caesar(cipher_text, max_totals)
		return clear_text

	def encode_vigenere(self, message, key):
		# Encode message using rotation by key string characters
		key_list = list(key)
		message_list = list(message)
		# Convert string form of key to list of integer shifts
		for index, char in enumerate(key_list):
			key_list[index] = self.letter_dict[char]
		# Iterate over unencoded message and rotate each letter by corresponding key shift
		for index,char in enumerate(message_list):
			message_list[index] = self.rotate_letter(char,key_list[index % (len(key_list))])
		cipher_text = ''.join(message_list)
		return cipher_text

	def decode_vigenere(self, cipher_text, key):
		# Decode ciphertext using rotation by key string characters
		key_list = list(key)
		message_list = list(cipher_text)
		for index, char in enumerate(key_list):
			key_list[index] = self.letter_dict[char]
		for index, char in enumerate(message_list):
			message_list[index] = self.rotate_letter(char, - key_list[index % (len(key_list))])
		clear_text = ''.join(message_list)
		return clear_text

	def encode_otp(self, message):
		# Similar to a vernan cipher, but we will generate a random key string and return it
		binary_numeric = string_to_binary(message)
		binary_string = binary_to_binary_string(binary_numeric)
		random_key = list()
		cipher_text	= list()
		# Create a random bit string, whose length is equal to length of message
		for i in range(len(binary_string)):
			random_key.append(get_random_bit())
		random_key = ''.join(random_key)
		# Create cipher text using XOR of message and key
		for i in range(len(random_key)):
			if int(random_key[i]) + int(binary_string[i]) == 1:
				cipher_text.append('1')
			else:
				cipher_text.append('0')
		cipher_text = ''.join(cipher_text)
		random_key = binary_string_to_binary(random_key)
		return cipher_text, random_key

	def decode_otp(self, cipher_text, key):
		# XOR cipher text and key. Convert result to string
		clear_text = list()
		key = binary_to_binary_string(key)
		# When there are leading zeroes, they will get erased
		# If and nested for  add the leading zeroes back
		if len(key) != len(cipher_text):
			difference = len(cipher_text) - len(key)
			key_list = list(key)
			for i in range(difference):
				key_list.insert(0,"0")
			key = ''.join(key_list)
		for i in range(len(cipher_text)):
			if int(cipher_text[i]) + int(key[i]) == 1:
				clear_text.append('1')
			else:
				clear_text.append('0')
		clear_text = ''.join(clear_text)
		clear_text = binary_string_to_binary(clear_text)
		clear_text = (binary_to_string(clear_text))
		return clear_text

	def read_wordlist(self):
		# Extra Credit: Read all words in wordlist and store in list. Remember to strip the endline characters
		filename = "wordlist.txt"

	def crack_vigenere(self, cipher_text):
		# Extra Credit: Break a vigenere cipher by trying common words as passwords
		# Return both the original message and the password used
		self.read_wordlist()
		return None, None


if __name__ == '__main__':
	print("---------------------TEST CASES---------------------------")
	cipher_suite = Cipher()
	print(cipher_suite.inverse_dict)
	print("---------------------PART 1: CAESAR-----------------------")
	message = read_message()
	cipher_text = cipher_suite.encode_caesar(message, 5)
	print('Encrypted Cipher Text:', cipher_text)
	decoded_message = cipher_suite.decode_caesar(cipher_text, 5)
	print('Decoded Message:', decoded_message)
	print("------------------PART 2: BREAKING CAESAR------------------")
	cracked = cipher_suite.crack_caesar(cipher_text)
	print('Cracked Code:', cracked)
	print("---------------------PART 3: Vignere----------------------")
	password = 'dog'
	print('Encryption key: ', password)
	cipher_text = cipher_suite.encode_vigenere(message, password)
	print('Encoded:', cipher_text)
	decoded_message = cipher_suite.decode_vigenere(cipher_text, password)
	print('Decoded:', decoded_message)


	print("-----------------------PART 4: OTP------------------------")

	cipher_text, key = cipher_suite.encode_otp(message)
	decoded = cipher_suite.decode_otp(cipher_text, key)
	print('Cipher Text:', cipher_text)
	print('Generated Key:', key)
	print('Decoded:', decoded_message)

	print('---------PART 5: Breaking Vignere (Extra Credit)----------')
	cipher_text = cipher_suite.encode_vigenere(message, password)
	cracked, pwrd = cipher_suite.crack_vigenere(cipher_text)
	print('Cracked Code:', cracked)
	print('Password:',pwrd)