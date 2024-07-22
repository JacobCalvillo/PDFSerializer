import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("/Users/jacob/OneDrive/Escritorio/Serializer/pdfserializer-firebase-adminsdk-dg309-30c99b3ca7.json")

firebase_admin.initialize_app(cred, {
    'storageBucket': 'pdfserializer.appspot.com'
})

bucket = storage.bucket()
