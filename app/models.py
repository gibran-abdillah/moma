from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime 
from sqlalchemy import extract
import time 

db = SQLAlchemy()

DEFAULT_MONTHS = datetime.utcnow().month


class BaseModel:
    def __commit(self):
        db.session.commit()
    
    def save(self):
        db.session.add(self)
        self.__commit()
    
    def delete(self):
        db.session.delete(self)
        self.__commit()
    

class Money(db.Model, BaseModel):
    __tablename__ = 'money'

    id = db.Column(db.Integer, primary_key=True)
    income = db.Column(db.Integer, default=0)
    outcome = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<income:{}>'.format(self.income)
    
    def to_dict(self) -> dict:
        data = {
                'income':self.income, 
                'outcome':self.outcome,
                'date':'{}/{}/{}'.format(self.date.day, self.date.month, self.date.year)
                }
        
        return data
    
    @classmethod
    def fetch_data(cls, month: int=DEFAULT_MONTHS):
        data = {}

        # thx for stackoverflow <3

        result = cls.query.filter(
                        extract('month', cls.date) == month).all()
        
        for res in result:
        
            date_format = res.date.strftime('%d/%m/%y')
            if date_format not in ' '.join(data.keys()):
                data[date_format] = {'income':[], 'outcome':[]}
                data[date_format]['income'].append(res.income)
                data[date_format]['outcome'].append(res.outcome)
            else:
                data[date_format]['income'].append(res.income)
                data[date_format]['outcome'].append(res.outcome)
                

        for key in data.keys():
            data[key]['inc_data'] = len(data[key]['income'])
            data[key]['out_data'] = len(data[key]['outcome'])

            sum_inc = sum(data[key]['income'])
            sum_out = sum(data[key]['outcome'])

            data[key]['income'] = sum_inc
            data[key]['outcome'] = sum_out

    
        return data