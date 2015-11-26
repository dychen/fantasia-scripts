import argparse
import os
from csv import reader

from sqlalchemy import create_engine, Column, ForeignKey, UniqueConstraint, \
    Integer, Unicode, String, Date
from sqlalchemy.orm import scoped_session, sessionmaker, column_property
from sqlalchemy.ext.declarative import declarative_base

DB_ENGINE = create_engine(os.environ['DATABASE_URL'], convert_unicode=True)
DB_SESSION = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=DB_ENGINE))
BASE = declarative_base()
#BASE.query = DB_SESSION.query_property()
print 'Initialized database session'

class Player(BASE):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    position = Column(String(2))
    team = Column(String(3))

    def __repr__(self):
        return '<Player %r>' % (self.name)

class Injury(BASE):
    __tablename__ = 'injury'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    status = Column(String(20))
    date = Column(Date)

    __table_args__ = (UniqueConstraint('player_id', 'date'),)

    def __repr__(self):
        return ('<Injury %r %r %s>'
                % (self.player.__repr__, self.date, self.status))

class InjuryComment(BASE):
    __tablename__ = 'injury_comment'

    id = Column(Integer, primary_key=True)
    injury_id = Column(Integer, ForeignKey('injury.id'), nullable=False)
    comment = Column(Unicode(500))

    def __repr__(self):
        return '<Injury %r %r %s>' % (self.injury.__repr__, self.comment)

def add_new(model, fields, unique_fields):
    query = DB_SESSION.query(model)
    for ufield in unique_fields:
        query = query.filter(getattr(Player, ufield)==fields[ufield])
    count = query.count() # Slow
    if count == 0:
        DB_SESSION.add(model(**fields))
        print 'Added model %s' % fields
    else:
        print 'Duplicate found %s' % fields

def init_db():
    print 'Creating database'
    BASE.metadata.create_all(bind=DB_ENGINE)

def seed_db_from_salaries(filename):
    print 'Seeding players from salary file %s' % filename
    with open(filename) as f:
        csvreader = reader(f, delimiter=',', quotechar='"')
        for i, row in enumerate(csvreader):
            if i != 0:
                pos, name, _, _, _, team = row
                add_new(Player, {
                    'name': unicode(name, encoding='utf-8'),
                    'position': pos,
                    'team': team
                }, ['name'])
    DB_SESSION.commit()

def drop_db():
    print 'Dropping database'
    BASE.metadata.drop_all(bind=DB_ENGINE)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_const', const=True,
                        help='Initialize database with existing DDL')
    parser.add_argument('--seed', type=str,
                        help='Seed database from salaries file')
    parser.add_argument('--drop', action='store_const', const=True,
                        help='Drop all tables in existing database')
    args = parser.parse_args()
    if args.drop:
        drop_db()
    if args.init:
        init_db()
    if args.seed:
        seed_db_from_salaries(args.seed)

