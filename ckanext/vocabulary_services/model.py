import datetime

from ckan.model import meta
from ckan.model import types as _types
from sqlalchemy import types, Column, Table
from ckan.model.domain_object import DomainObject


vocabulary_service_table = Table('vocabulary_service', meta.metadata,
                         Column('id', types.UnicodeText,
                                primary_key=True,
                                default=_types.make_uuid),
                         Column('type', types.UnicodeText,
                                nullable=False),
                         Column('name', types.UnicodeText,
                                nullable=False),
                         Column('uri', types.UnicodeText,
                                nullable=False),
                         Column('update_frequency', types.UnicodeText,
                                nullable=False),
                         Column('date_created', types.DateTime,
                                default=datetime.datetime.utcnow()),
                         Column('date_modified', types.DateTime,
                                default=datetime.datetime.utcnow()),
                         Column('date_last_processed', types.DateTime),
                         )

vocabulary_service_term_table = Table('vocabulary_service_term', meta.metadata,
                                      Column('id', types.UnicodeText,
                                             primary_key=True,
                                             default=_types.make_uuid),
                                      Column('vocabulary_service_id', types.UnicodeText,
                                             nullable=False),
                                      Column('label', types.UnicodeText,
                                             nullable=False),
                                      Column('uri', types.UnicodeText,
                                             nullable=False),
                                      Column('date_created', types.DateTime,
                                             default=datetime.datetime.utcnow()),
                                      Column('date_modified', types.DateTime,
                                             default=datetime.datetime.utcnow()),
                                      )


class VocabularyService(DomainObject):
    """A VocabularyService object represents an external vocabulary
    used for populating and controlling a metadata schema field"""
    def __init__(self, type=None, name=None, uri=None, update_frequency=None):
        self.type = type
        self.name = name
        self.uri = uri
        self.update_frequency = update_frequency

    @classmethod
    def get(cls, reference):
        '''Returns a VocabularyService object referenced by its id or name.'''
        query = meta.Session.query(cls).filter(cls.id == reference)
        vocabulary_service = query.first()
        if vocabulary_service is None:
            vocabulary_service = cls.by_name(reference)
        return vocabulary_service

    @classmethod
    def all(cls):
        """
        Returns all vocabularies.
        """
        q = meta.Session.query(cls)

        return q.order_by(cls.name).all()


class VocabularyServiceTerm(DomainObject):
    """A VocabularyServiceTerm object represents a term from an external vocabulary
    used for populating and controlling a metadata schema field"""
    def __init__(self, vocabulary_service_id=None, label=None, uri=None):
        self.vocabulary_service_id = vocabulary_service_id
        self.label = label
        self.uri = uri

    @classmethod
    def get(cls, reference):
        '''Returns a VocabularyServiceTerm object referenced by its id.'''
        query = meta.Session.query(cls).filter(cls.id == reference)
        vocabulary_service_term = query.first()

        return vocabulary_service_term

    @classmethod
    def all(cls, vocabulary_service_id):
        """
        Returns all terms for a vocabulary service.
        """
        q = meta.Session.query(cls).filter(cls.vocabulary_service_id == vocabulary_service_id)

        return q.order_by(cls.label).all()


meta.mapper(VocabularyService, vocabulary_service_table)
meta.mapper(VocabularyServiceTerm, vocabulary_service_term_table)

