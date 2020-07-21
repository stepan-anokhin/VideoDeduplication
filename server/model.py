from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Table, Column, String, MetaData,Integer,Binary,Boolean,Float,ARRAY

from app import db

Base = db.Model

class Signature(Base):
    
    __tablename__ = 'signatures'
    id = Column(Integer,primary_key=True)
    original_filename = Column(String)
    signature = Column(Binary)

    def to_json(self):

        json_signature = {
            'id': self.id,
            'original_filename': self.original_filename
        }
        return json_signature
    

# TODO:Revaluate which columns are actually essential
# TODO: Add sha signature

class VideoMetadata(Base):
    
    __tablename__ = 'videometadata'

    original_filename = Column(String,primary_key=True)
    video_length = Column(Float)
    avg_act = Column(Float)
    video_avg_std = Column(Float)
    video_max_dif = Column(Float)
    gray_avg = Column(Float)
    gray_std = Column(Float)
    gray_max = Column(Float)
    video_duration_flag = Column(Boolean)
    video_dark_flag = Column(Boolean)
    flagged = Column(Boolean)

    def to_json(self):

        json_videometadata = {
            "original_filename" : self.original_filename,
            "video_length" : self.video_length,
            "avg_act" : self.avg_act,
            "video_avg_std" : self.video_avg_std,
            "video_max_dif" : self.video_max_dif,
            "gray_avg" : self.gray_avg,
            "gray_std" : self.gray_std, 
            "gray_max ": self.gray_max,
            "video_duration_flag": self.video_duration_flag,
            "video_dark_flag ": self.video_dark_flag,
            "flagged" : self.flagged
        }

        return json_videometadata



class Scenes(Base):

    __tablename__ = 'scenes'
    original_filename = Column(String,primary_key=True)
    video_duration_seconds = Column(Float)
    avg_duration_seconds = Column(Float)
    scene_duration_seconds = Column(ARRAY(Integer))
    scenes_timestamp = Column(ARRAY(String))
    total_video_duration_timestamp = Column(String)


    def to_json(self):

        json_scenes = {
            "original_filename" : self.original_filename,
            "video_duration_seconds" : self.video_duration_seconds,
            "avg_duration_seconds" : self.avg_duration_seconds,
            "scene_duration_seconds" : self.scene_duration_seconds,
            "scenes_timestamp" : self.scenes_timestamp,
            "total_video_duration_timestamp":self.total_video_duration_timestamp
        }

        return json_scenes