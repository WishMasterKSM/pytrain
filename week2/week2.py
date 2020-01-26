from configparser import ConfigParser
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from hospital import Base
from hospital import Hospital
from doctor import Doctor

from lxml import etree

engine = create_engine('postgresql://python:python@ch9378/python_db')
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

def singleton(cls):
    instances = {}
    def create(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return create

@singleton
class TaskCounter:
    counter = 0

    def getTaskNumber(self):
        self.counter += 1
        return self.counter

def task_divider(func):
    def inner(*args, **kwargs):
        border = "-"
        header = border * 15
        taskCounter = TaskCounter()
        task_num = taskCounter.getTaskNumber()
        print(f'{header}{task_num}{header}')
        func(*args, **kwargs)
        print(border * 31)
    return inner
 
def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

@task_divider
def connect():
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        sql_str = open("preparedb.sql", "r").read()
        cur.execute(sql_str)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

@task_divider
def sql_task1():
    name = input("Enter hospital or doctor name: ")
    s = session()
    hospital_found = True
    try:
        h = s.query(Hospital).filter(Hospital.hospital_name == name).all()
        if not h:
            hospital_found = False;
        else:
            print(h)
    except exc.SQLAlchemyError as e:
        print(e)
    
    if not hospital_found:
        try:
            d = s.query(Doctor).filter(Doctor.doctor_name == name).all()
            if not d:
                print('Nothing has been found')
            else:
                print(h)
        except exc.SQLAlchemyError as e:
            print(e)
    s.close()

@task_divider
def sql_task2():
    spec = input("Enter speciality: ")
    s = session()
    try:
        d = s.query(Doctor).filter(Doctor.speciality == spec).all()
        if not d:
            print('Nothing has been found')
        else:
            print(d)
    except exc.SQLAlchemyError as e:
        print(e)
    s.close()

@task_divider
def sql_task3():
    hospital_name = input("Enter hospital name: ")
    s = session()
    try:
        d = s.query(Doctor).filter(Doctor.hospital.has(hospital_name = hospital_name)).all()
        if not d:
            print('Nothing has been found')
        else:
            print(d)
    except exc.SQLAlchemyError as e:
        print(e)
    s.close()

@task_divider
def sql_task4():
    doctor_name = input("Enter doctor name: ")
    s = session()
    try:
        d = s.query(Doctor).filter(Doctor.doctor_name == doctor_name).one()
        exp = input("Enter doctor experience: ")
        d.experience = exp
        s.commit()
        print('Experience updated')
    except exc.SQLAlchemyError as e:
        print(e)
    s.close()

@task_divider
def create_xml():
    s = session()
    eroot = etree.Element("Envelope")
    eroot.set("xmlns", "http://schemas.xmlsoap.org/soap/envelope/")
    ebody = etree.SubElement(eroot, "Body")
    edoctors = etree.SubElement(ebody, "Doctors")
    try:
        d = s.query(Doctor).order_by(Doctor.doctor_id).all();
        for doctor in d:
            edoctor = etree.SubElement(edoctors, "Doctor")
            eid = etree.SubElement(edoctor, "Doctor_ID")
            eid.text = '{}'.format(doctor.doctor_id)
            edata = etree.SubElement(edoctor, "Personal_Data")
            ename = etree.SubElement(edata, "Name")
            ename.text = doctor.doctor_name
            espec = etree.SubElement(edata, "Speciality")
            espec.text = doctor.speciality
            esal = etree.SubElement(edata, "Salary")
            esal.text = '{}'.format(doctor.salary)
    except exc.SQLAlchemyError as e:
        print(e)
    et = etree.ElementTree(eroot)
    et.write('doctors.xml', encoding='UTF-8', pretty_print=True, xml_declaration=True)
    print('Xml file created')
    s.close()

def main():
    connect()
    create_xml()
    sql_task1()
    sql_task2()
    sql_task3()
    sql_task4()

if __name__ == '__main__':
    main()