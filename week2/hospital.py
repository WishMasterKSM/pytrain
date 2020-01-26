from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hospital(Base):
    __tablename__ = 'hospital'
    hospital_id = Column(Integer, primary_key=True)
    hospital_name = Column(String)
    bed_count = Column(Integer)

    def __str__(self):
        return 'Hospital name=\'{}\' bed_count={}'.format(self.hospital_name, self.bed_count)
    
    def __repr__(self):
        return str(self)
