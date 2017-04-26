#!/usr/bin/env python3.6

from re import match
from shemutils.logger import Logger
from sys import exit
from os import system
from time import sleep


logger = Logger("Decryptor")

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
COMMAND_PREFIX = "[Decryptor] @> "
RED = "\033[91m"
GRN = "\033[92m"
GRE = "\033[2m"
END = "\033[0m"

def red(i):
    return RED + i + END

def green(i):
    return GRN + i + END

def grey(i):
    return GRE + i + END


class Decryptor(object):
    def __init__(self):
        self.data = None
        self.key = None
        self.translate = False
        self._start()

    def _parse_callback(self, message):
        if message is bytes:
            message = message.decode()

        regex_set_cipher = 'set cipher "(?P<cipher>[a-zA-Z0-9,_\.\-:\s]+)"'
        regex_toggle_translate = 'toggle translate'
        regex_substitution = 'set (?P<letter>[a-zA-Z0-9]+)\s+=\s+(?P<cipher>[a-zA-Z0-9\*]+)'


        set_cipher = match(regex_set_cipher, message)
        toggle_translate = match(regex_toggle_translate, message)
        substitute = match(regex_substitution, message)

        if set_cipher:
            self.data = set_cipher["cipher"].lower()
            return 0

        if toggle_translate:
            self.translate = not self.translate
            return 0

        if substitute:
            letter = substitute["letter"].upper()
            cipher_letter = substitute["cipher"].upper()
            self.key[letter] = cipher_letter
            return 0
        return 1

    def _clean_screen(self):
        return system("clear")

    def _parse_unknown(self):
        new_data = self.data
        unknown_letters = list()
        new_data = new_data.replace("m", grey("m"))

        for key in self.key:
            char = key.lower()
            if self.key[key] == "*":
                if char == "m":
                    continue
                new_data = new_data.replace(char, grey(char))
            else:
                dec_char = self.key[key]
                new_data = new_data.replace(char, green(dec_char))
        return new_data

    def _round(self):
        self._clean_screen()
        if self.data is not None:
            color_data = self._parse_unknown()
            print("Current status: {0}\n\n".format(color_data))
        else:
            print("Currant status: %s\n\n" % "No cipher set")
        print("Model Alphabet: {0}".format('|'.join(list(ALPHABET))))
        print("Cipher Alphab.: {0}".format('|'.join(self.key.values())))

        operator_data = input(COMMAND_PREFIX)
        if self._parse_callback(operator_data) != 0:
            print("Unknown command.")
        sleep(1.5)

    def _start(self):
        self.key = self._alphabet_generate()
        while 1 == 1:
           self._round()

    def _alphabet_generate(self):
        unknown_alphabet = dict()
        for char in ALPHABET:
            unknown_alphabet[char] = "*"
        return unknown_alphabet


if __name__ == "__main__":
    dec = Decryptor()

