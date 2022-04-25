import requests

def get_Images(filename1,filename2 ,url):
  image_file_descriptor1= open(filename1, 'rb')
  image_file_descriptor2 = open(filename2, 'rb')

  # Requests makes it simple to upload Multipart-encoded files
  files = {'video1': image_file_descriptor1,'video2': image_file_descriptor1}
  response = requests.post(url, files=files)
  image_file_descriptor1.close()
  image_file_descriptor2.close()

  #Check status
  if response.status_code == 200:
    return response.json()
  return f'Error - status code {response.status_code}'

url = 'http://127.0.0.1:5000/classify_image' #change this url for the appropiate url
images = get_Images('uploads/video1.mp4','uploads/video2.mp4', url)
#After you receive the list of images you might need to decode the images
