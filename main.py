from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Query
import uvicorn
import os
from dotenv import load_dotenv
import openai


app = FastAPI()


load_dotenv()


openai.api_key = os.environ.get("OPENAI_API_KEY")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get_course_content/")
async def new_user(info : Request):

    print(await info.body())
    infoDict = await info.json()
    infoDict = dict(infoDict)

    prompt = f'''Act like an instructor and content creator, create content for high school students for the following details:
    Topic or Title : {infoDict["Topic"]}
    Student grade level : {infoDict["Grade"]}
    Learning style : {infoDict["Style"]}
    Learning Speed  : {infoDict["Speed"]}
    Student interests : {infoDict["Interests"]}
    Available time : {infoDict["Time"]}
    Future goals : {infoDict["FutureGoals"]}
    Note: generate the content structue accordinly to the time line given above?
    '''

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=2500,
        n=1,
        stop=None,
    )

    return {"Content" : str(response.choices[0]["text"]) }


