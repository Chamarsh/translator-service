from src.translator import translate_content, client
from mock import patch

def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == 'This is a Chinese message'

def test_llm_normal_response():
    is_english, translated_content = translate_content("This is an English message")
    assert is_english == True
    assert translated_content == 'This is an English message'

@patch.object(client.chat.completions, 'create')
def test_unexpected_language(mocker):
    mocker.return_value.choices[0].message.content = ""

    response = translate_content("Hier ist dein erstes Beispiel.")
    assert response[1] == "Empty response detected"

@patch.object(client.chat.completions, 'create')
def test_malformed_response(mocker):
    mocker.return_value.choices[0].message.content = "Unexpectedresult!@@@"

    response = translate_content("Wie kann ich Ihnen helfen?")
    assert response[1] == "Incorrect response format detected"

@patch.object(client.chat.completions, 'create')
def test_empty_response(mocker):
    mocker.return_value.choices[0].message.content = "This is not correct"

    response = translate_content("Esta es una gran sugerencia.")
    assert response[1] == "Malformed response format detected"

@patch.object(client.chat.completions, 'create')
def test_incorrect_format_response(mocker):
    mocker.return_value.choices[0].message.content = '{"error": "unexpected format"}'

    response = translate_content("Questa funzione non è attualmente disponibile.")
    assert response[1] == "Malformed response format detected"