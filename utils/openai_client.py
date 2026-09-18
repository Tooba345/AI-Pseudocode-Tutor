import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as file:
            self.system_prompt = file.read()

    def ask(self, prompt, image_path=None):
        try:
            if image_path:
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(
                        image_file.read()
                    ).decode("utf-8")

                response = self.client.responses.create(
                    model="gpt-5.6-luna",
                    instructions=self.system_prompt,
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": prompt
                                },
                                {
                                    "type": "input_image",
                                    "image_url": f"data:image/jpeg;base64,{image_data}"
                                }
                            ]
                        }
                    ]
                )

            else:
                response = self.client.responses.create(
                    model="gpt-5.6-luna",
                    instructions=self.system_prompt,
                    input=prompt
                )

            return response.output_text

        except Exception as e:
            return f"❌ OpenAI error:\n{e}"