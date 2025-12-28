from database import Base
from sqlalchemy import Column, Integer, String, Float

class Feature(Base):
    __tablename__ = "Song_Features"
    
    id = Column(Integer, primary_key = True)
    filename = Column(String)
    rms = Column(Float)
    tempo = Column(Float)

    mfcc1 = Column(Float)
    mfcc2 = Column(Float)
    mfcc3 = Column(Float)
    mfcc4 = Column(Float)
    mfcc5 = Column(Float)
    mfcc6 = Column(Float)
    mfcc7 = Column(Float)
    mfcc8 = Column(Float)
    mfcc9 = Column(Float)
    mfcc10 = Column(Float)
    mfcc11 = Column(Float)
    mfcc12 = Column(Float)
    mfcc13 = Column(Float)