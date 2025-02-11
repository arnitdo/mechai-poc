from dotenv import load_dotenv
from google import genai
from google.genai import types

import os

load_dotenv()

file = open("tests/solder.mp4", "rb")
file_bytes = file.read()
file.close()

client = genai.Client(
	vertexai = True,
	location = os.getenv("GCP_LOCATION"),
	# api_key = os.getenv("GCP_API_KEY"),
	project = os.getenv("GCP_PROJECT"),
)

output_schema = types.Schema(
	type = types.Type.ARRAY,
	items = types.Schema(
		type = types.Type.OBJECT,
		properties = {
			"activity": {
				"type": types.Type.STRING,
				"description": "The activity performed ONE WORD"
			},
			"start_timestamp_ms": {
				"type": types.Type.NUMBER,
				"description": "Start timestamp of the activity in milliseconds"
			},
			"end_timestamp_ms": {
				"type": types.Type.NUMBER,
				"description": "End timestamp of the activity in milliseconds"
			}
		},
		required = ["activity", "start_timestamp_ms", "end_timestamp_ms"]
	)
)

response = client.models.generate_content(
    model="gemini-2.0-flash-001", 
	contents = [
		types.Part.from_bytes(data = file_bytes, mime_type = "video/mp4"),
		types.Part.from_text(text = "Respond in the given schema")
	],
	config = types.GenerateContentConfig(
		system_instruction = [
			"You are an expert at industrial systems",
			"Your task is to observe a video and provide a structured output for each activity that is performed - activity, start_timestamp_ms and end_timestamp_ms"
		],
		response_schema = output_schema,
		response_mime_type = "application/json"
	),

)
print(response, response.text)