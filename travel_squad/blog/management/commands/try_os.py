import os

dir = '../../../media/photos'

files = os.listdir('../../../media/photos')
images = list(filter(lambda x: x.endswith('.jpg'),files))
print(images)