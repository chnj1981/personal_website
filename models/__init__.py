from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()


def timestamp_format(t):
    format = '%Y/%m/%d %H:%M:%S'
    v = t + 3600 * 8
    valuegmt = time.gmtime(v)
    return time.strftime(format, valuegmt)


def timestamp():
    return int(time.time())


class ModelMixin(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls, desc=True):
        if desc:
            return cls.query.order_by(cls.id.desc()).all()
        return cls.query.order_by(cls.id).all()
