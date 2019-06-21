from datetime import datetime
import xlrd
from sqlalchemy import Column, String, create_engine, Integer, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_staff_data():
    excel = xlrd.open_workbook('staff.xlsx')
    sheet = excel.get_by_index(0)
    c = 1
    rows = []
    try:
        while c:
            pre = sheet.row_values(c)
            pre[6] = datetime.strptime(pre[6], '%Y-%m-%d')
            pre[6] = datetime.strptime(pre[6], '%')
            rows.append()
    except IndexError as _:
        return rows


class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(33), nullable=False)
    position = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    phone = Column(String(15))
    gender = Column(String(8))
    id_card = Column(String(18))
    age = Column(Integer)
    birthday = Column(Date)
    emergency = Column(String(33))
    emergency_num = Column(String(15))
    address = Column(String(256))
    hiredate = Column(Date)
    degree = Column(String(32))
    bank_num = Column(String(20))


engine = create_engine('mysql+pymysql://root:123918@localhost:3306/aston')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
# new_staff = Staff(id=3, name='aston')
session.add(Staff(name='dante'))

session.commit()
session.close()
