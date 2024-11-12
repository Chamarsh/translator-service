from openai import AzureOpenAI

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY, 
    api_version="2024-02-15-preview",
    azure_endpoint="https://openai-the-bots.openai.azure.com/"  # Replace with your Azure endpoint
)

def translate_content(post: str) -> tuple[bool, str]:
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {
                "role": "system",
                "content": "You are a translator who can translate non-English text to English. I need you to first classify what language I am giving you. Return True if it is English and False if not."
            }, {
                "role": "user",
                "content": post
            }, {
                "role": "system",
                "content": "If the language is English return True and the english text if it is not English return False and the translated text. An example response is 'True This is the english sentence' and another is 'False This is the translated sentence'. Do not add a period at the end of the sentence."
            }
        ]
    )

    output = response.choices[0].message.content
    if len(output) == 0:
        return (False, "Empty response detected")
    if len(output.split(" ")) == 1:
        return (False, "Incorrect response format detected")
    res = output.split(" ", 1)
    lang, text = res[0], res[1]

    if lang != 'True' and lang != 'False':
        return (False, "Malformed response format detected")

    if lang == "True":
        return (True, text)
    return (False, text)