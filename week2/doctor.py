from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from hospital import Base
from hospital import Hospital

class Doctor(Base):
    __tablename__ = 'doctor'
    doctor_id = Column(Integer, primary_key=True)
    doctor_name = Column(String)
    hospital_id = Column(Integer, ForeignKey(Hospital.hospital_id))
    hospital = relationship(Hospital)
    joining_date = Column(Date)
    speciality = Column(String)
    salary = Column(Integer)
    experience = Column(Integer)

    def __str__(self):
        return 'Doctor name=\'{}\' hospital=\'{}\''.format(self.doctor_name, self.hospital.hospital_name)

    def __repr__(self):
        return str(self)
