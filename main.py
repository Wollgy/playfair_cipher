"""
@author: libor_komanek
"""
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from unidecode import unidecode
from string import ascii_uppercase

qtCreatorFile = "PlayfairCipher.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def replaceLanguageSpecificCharacters(text: str, lang: str = "en") -> str:
    """Replaces a single character in the given string with another based on specified language.
    Raises Exception if the provided language is not a valid value.

    :param text: original text
    :param lang: language used for the encryption; valid values are "en" and "cs"
    :return: string with replaced characters for the specified language
    """
    text = text.upper()
    if lang == "en":
        return text.replace("J", "I")
    elif lang == "cs":
        return text.replace("Q", "O")
    else:
        raise ValueError("Invalid language specified.")


def filterKey(key: str, language: str = "en") -> str:
    """Filters the given cipherkey. That includes converting to unicode characters, removing any non alpha characters,
    removing duplicate characters and replacing a single character specific for the given language.

    :param key: the cipherkey used to create cipher matrix
    :param language: language used for the encryption; valid values are "en" and "cs"
    :return: filtered key in the correct format
    """
    key = unidecode(key).upper()
    key = "".join(char for char in key if char.isalpha())  # only leave letters
    key = "".join(dict.fromkeys(key))  # remove duplicate characters
    key = replaceLanguageSpecificCharacters(key, language)
    return key


def generateCipherMatrix(key: str, language: str = "en") -> list[list[str]]:
    """Generates the cipher matrix as a 2D list using the given key and language.

    :param key: the cipherkey used to create cipher matrix
    :param language: language used for the encryption; valid values are "en" and "cs"
    :return: cipher matrix as a 2D list
    """
    key = filterKey(key, language)
    alphabet: str = key + replaceLanguageSpecificCharacters(ascii_uppercase, language)  # valid characters
    alphabet = "".join(dict.fromkeys(alphabet))  # remove duplicates
    # Generate 5x5 matrix filled with letters from alphabet
    rows: int = 5
    cols: int = 5
    matrix: list[list[str]] = [[alphabet[i + rows * j] for i in range(cols)] for j in range(rows)]
    return matrix


def filterPlainText(text: str, language: str = "en") -> str:
    """Filters the given plain text. That includes converting it to uppercase unicode,
    replacing spaces and digits with their string representations, removing any left non alpha characters after that
    and replacing specific character occurences based on the specified language.

    :param text: plain text entering into encryption
    :param language: language used for the encryption; valid values are "en" and "cs"
    :return: filtered plain text
    """
    text = unidecode(text).upper()
    text = text.replace(" ", "XSPACEX")\
        .replace("0", "XZEROX")\
        .replace("1", "XONEX")\
        .replace("2", "XTWOX")\
        .replace("3", "XTHREEX")\
        .replace("4", "XFOURX")\
        .replace("5", "XFIVEX")\
        .replace("6", "XSIXX")\
        .replace("7", "XSEVENX")\
        .replace("8", "XEIGHTX")\
        .replace("9", "XNINEX")
    text = "".join(char for char in text if char.isalpha())  # remove special characters
    text = replaceLanguageSpecificCharacters(text, language)
    return text


def convertStringRepresentationsBack(cipher_text: str) -> str:
    """Replaces space and digit string representations back to their original form.

    :param cipher_text: cipher text entering into decryption
    :return: original text with replaced string representations
    """
    cipher_text = cipher_text.replace("XSPACEX", " ")\
        .replace("XZEROX", "0")\
        .replace("XONEX", "1")\
        .replace("XTWOX", "2")\
        .replace("XTHREEX", "3")\
        .replace("XFOURX", "4")\
        .replace("XFIVEX", "5")\
        .replace("XSIXX", "6")\
        .replace("XSEVENX", "7")\
        .replace("XEIGHTX", "8")\
        .replace("XNINEX", "9")
    return cipher_text


def fillPlainTextWithExtraCharacters(text: str) -> str:
    """Checks for pairs of identical characters in a string and inserts "W" or "X" as required so that no pair
    is identical. Also inserts another extra character at the end of the string if the last pair is not complete.

    :param text: the original text to be prepared for conversion to digraphs
    :return: plain text with extra characters prepared for conversion to digraphs
    """
    result: str = ""
    for i in range(len(text) - 1):
        result += text[i]
        if text[i] == text[i + 1] and len(result) % 2 != 0:
            # If adding W results in another identical pair, add X instead
            result += ("W" if text[i] != "W" else "X")
    result += text[-1]  # add the last ommitted character from the original text
    if len(result) % 2 != 0:  # additional character if the last character is not in a pair
        result += ("X" if result[-1] != "X" else "W")
    return result


def convertTextToDigraphs(text: str) -> list[str]:
    """Converts the given string to a list of pairs of characters.

    :param text: the text to be converted into a list of digraphs
    :return: digraphs as a list
    """
    digraphs: list[str] = []
    tmp: int = 0
    for i in range(2, len(text) + 1, 2):
        digraphs.append(text[tmp:i])
        tmp = i
    return digraphs


def getPositionInMatrix(char: str, matrix: list[list[str]]) -> tuple[int, int]:
    """Returns both coords of the specified character in the given cipher matrix, which has the form of a 2D list.
    Raises and exception if the character could not be found in the given matrix.

    :param char: the character whose coords you are looking for
    :param matrix: the 5x5 cipher matrix as a 2D list to be searched
    :return: the two indexes of the character in the form of tuple as (row, col)
    """
    for row in range(5):
        if char in matrix[row]:
            col = matrix[row].index(char)
            return row, col
    raise ValueError(
        "There is likely a problem in input filtering. The specified character could not be found in the matrix.")


def groupCharacters(text: str, n: int) -> str:
    """
    Returns the original string with spaces between groups of N characters.
    :param text: original string
    :param n: number of characters in every group
    :return: string with grouped characters
    """
    result: str = ' '.join([
        text[i:i + n] for i in range(0, len(text), n)
    ])
    return result


def encrypt(key: str,
            plain_text: str,
            language: str = "en",
            matrix: list[list[str]] = None) -> str:
    """Encrypts the given plain text using Playfair cipher. The resulting cipher text is capable of storing
    alpha characters, but also spaces and digits through the use of their string representations.

    :param key: cipher key used for generating the cipher matrix
    :param plain_text: message to be encrypted
    :param language: language of the message - valid values "en" and "cs" - defaults to "en"
    :param matrix: cipher matrix - optional argument intended to avoid generating the matrix twice when used with GUI
    :return: encrypted message
    """
    if matrix is None:
        matrix = generateCipherMatrix(key, language)
    plain_text = filterPlainText(plain_text)
    plain_text = fillPlainTextWithExtraCharacters(plain_text)
    digraphs: list[str] = convertTextToDigraphs(plain_text)

    cipher_text: str = ""
    for char1, char2 in digraphs:
        row1, col1 = getPositionInMatrix(char1, matrix)
        row2, col2 = getPositionInMatrix(char2, matrix)
        if row1 == row2:  # row rule
            cipher_text += matrix[row1][(col1 + 1) % 5] + matrix[row1][(col2 + 1) % 5]
        elif col1 == col2:  # column rule
            cipher_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col1]
        else:  # rectangle
            cipher_text += matrix[row1][col2] + matrix[row2][col1]
    return cipher_text


def decrypt(key: str,
            cipher_text: str,
            language: str = "en",
            matrix: list[list[str]] = None) -> str:
    """Decrypts the given cipher text using Playfair cipher. The resulting message has unicode letters, digits
    and spaces in the same places as before encryption.

    :param key: cipher key used for generating the cipher matrix
    :param cipher_text: encrypted message to be decrypted
    :param language: language of the message - valid values "en" and "cs" - defaults to "en"
    :param matrix: cipher matrix - optional argument intended to avoid generating the matrix twice when used with GUI
    :return: decrypted message
    """
    if matrix is None:
        matrix = generateCipherMatrix(key, language)
    cipher_text = cipher_text.replace(" ", "")
    if len(cipher_text) % 2 != 0:
        raise ValueError("The specified cipher text is invalid and cannot be decrypted.")
    digraphs: list[str] = convertTextToDigraphs(cipher_text)

    plain_text: str = ""
    for char1, char2 in digraphs:
        row1, col1 = getPositionInMatrix(char1, matrix)
        row2, col2 = getPositionInMatrix(char2, matrix)
        if row1 == row2:  # row rule
            plain_text += matrix[row1][(col1 - 1) % 5] + matrix[row1][(col2 - 1) % 5]
        elif col1 == col2:  # column rule
            plain_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col1]
        else:  # rectangle
            plain_text += matrix[row1][col2] + matrix[row2][col1]
    plain_text = convertStringRepresentationsBack(plain_text)
    return plain_text


class PlayfairCipher(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Playfair cipher")
        self.execute_button.clicked.connect(self.execute)

    def execute(self):
        """
        Checks user input from GUI and calls appropriate function.
        """
        try:
            key: str = self.key.text()
            input_text: str = self.input_field.toPlainText()
            language: str = ("en" if self.english_radio.isChecked() else "cs")
            if len(key) < 1 or len(input_text) < 1:
                raise ValueError("Key and input fields cannot be empty!")

            matrix: list[list[str]] = generateCipherMatrix(key, language)
            output_text: str = (groupCharacters(encrypt(key, input_text, language, matrix), 5)
                                if self.encrypt_radio.isChecked()
                                else decrypt(key, input_text, language, matrix))
            self.fillMatrix(matrix)
            self.output_field.setPlainText(output_text)
        except Exception as e:
            self.output_field.setPlainText(f"Something went wrong! {str(e)}")

    def fillMatrix(self, matrix: list[list[str]]):
        """Fills the labels in GUI used to represent the cipher matrix with appropriate values.

        :param matrix: 5x5 cipher matrix
        """
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                self.findChild(QLabel, f"table_item_{row+1}{col+1}")\
                    .setText(matrix[row][col])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlayfairCipher()
    window.show()
    sys.exit(app.exec())
