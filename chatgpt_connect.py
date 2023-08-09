import openai


def connectToGPT(postLink):
    openai.api_key = "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"

    model_engine = "text-davinci-003"
    prompt = "please suggest a comment for "+ postLink
    print(prompt)


    completion = openai.Completion.create(
        engine = model_engine,
        prompt = prompt,
        max_tokens = 1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response.strip()