#Este arquivo define um DAO (Data Access Object), que é um padrão de design utilizado paraabstrair e encapsular o acesso a dados. 
# O BaseDAO é uma classe base para gerenciar a sessão do banco de dados.

# Gerenciamento de Sessão: A classe gerencia a criação, o commit e o fechamento da sessão do banco de dados. 
# Isso é importante para garantir que as operações de banco de dados sejam realizadas corretamente e que os recursos sejam liberados após o uso.

# Context Manager: O uso de __enter__ e __exit__ permite que a classe seja usada com o operador with em Python, garantindo que os recursos sejam gerenciados automaticamente.

from models.db_credentials import get_session
from sqlalchemy.exc import IntegrityError

class BaseDAO(object):
    """
    A Base class for all managers. Automatically handles session creation,
    the commiting and closing the connections.
    """
    def __init__(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Constructor
        """
        self._session = get_session() if (not session) else session
        self._commit_on_exit = commit_on_exit
        self._close_on_exit = close_on_exit

    def __enter__(self):
        """
        On enter
        """
        return self

    def __exit__(self, *exc_info):
        """
        On exit
        """
        if (self._session and self._commit_on_exit):
            try:
                # Connection must be closed when an exception happens here
                self._session.commit()
            except IntegrityError as e:
                self._session.close()
                raise e
        if (self._session and self._close_on_exit):
            self._session.close()

    def session(self):
        """
        Returns the session
        """
        return self._session
