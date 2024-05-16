import os


class Config:    
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db:5432/file_uploads_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    UPLOAD_FOLDER = 'uploads/'