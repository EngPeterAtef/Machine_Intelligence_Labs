from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file, read_word_list

"""
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
"""
DechiperResult = Tuple[str, int, int]


def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    """
    This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
    It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary.
    """

    def decipher(shift: int,n):
        deciphered_text = ""
        for i in range(n):
            if ciphered[i].isalpha():
                shifted_char = chr(
                    (ord(ciphered[i]) - ord("a") - shift) % 26 + ord("a")
                )
                deciphered_text += shifted_char
            else:
                deciphered_text += ciphered[i]
        words = deciphered_text.split()
        count_non_english_words = sum((1 for word in words if not word in dictionary))
        return (deciphered_text, shift, count_non_english_words)
    ciphered_words = ciphered.split() #list of words
    sub_ciphered = " ".join(ciphered_words[:min(50,int(len(ciphered_words)*0.5))]) #join half of the words in a string
    temp = min((decipher(shift,len(sub_ciphered)) for shift in range(26)), key=lambda x: x[2]) #use half of the words to get the shift key
    return decipher(temp[1],len(ciphered)) #use the shift key to get the answer

