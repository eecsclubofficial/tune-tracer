from database import Base
from sqlalchemy import Column, Integer, String, Float

class Feature(Base):
    __tablename__ = "Song_Features"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)

    mfcc_mean_2 = Column(Float)
    mfcc_mean_4 = Column(Float)
    mfcc_mean_7 = Column(Float)

    zcr_mean = Column(Float)
    event_density_mean = Column(Float)
    chroma_mean_7 = Column(Float)
