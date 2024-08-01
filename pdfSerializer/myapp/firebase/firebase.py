import firebase_admin
from firebase_admin import credentials, storage, auth

cred = credentials.Certificate("/Users/jacob/OneDrive/Escritorio/Serializer/pdfserializer-firebase-adminsdk-dg309-3fe1c3e6df.json")

firebase_admin.initialize_app(cred, {
    'storageBucket': 'pdfserializer.appspot.com'
})

bucket = storage.bucket()
