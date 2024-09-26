from openai import OpenAI
client = OpenAI()

ai_image = client.images.generate(
  model="dall-e-2",
  prompt="a white siamese cat",
  size="1024x1024",
  n=1,
)

image_url = ai_image.data[0].url
print(image_url)