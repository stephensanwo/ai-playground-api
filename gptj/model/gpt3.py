import requests


class GPTJ():

    def generate(context, token_max_length, temperature, top_probability):
        payload = {"context": str(context), "token_max_length": token_max_length,
                   "temperature": temperature, "top_p": top_probability}

        try:
            URL = requests.post(
                "http://api.vicgalle.net:5000/generate", params=payload)

            text = URL.json()
            return str(text['text'].split("Human")[0])

        except:
            return "GPT-J-6b is currently offline, please try again later"


if __name__ == "__main__":
    res = GPTJ.generate(context="""Human: Hello! Bot:""",
                        token_max_length=128, temperature=1.0, top_probability=0.9)

    # res = generate(context="""English: Hello! Spanish:""",
    #                token_max_length=128, temperature=1.0, top_probability=0.9)
    print(res)
