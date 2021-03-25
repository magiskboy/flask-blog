from google.cloud import storage

client = storage.Client()
bucket = client.bucket('flask-blog-profile-pics')
blob = bucket.blob('default.jpg')

with open('./app/static/main/profile_pics/default.jpg', 'rb') as f:
    blob.upload_from_file(f)

blob.make_public()
print('Done', blob.media_link)
