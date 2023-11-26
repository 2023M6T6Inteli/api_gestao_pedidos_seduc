# Este arquivo define um DAO (Data Access Object), que é um padrão de design utilizado para abstrair e encapsular o acesso a dados. 
# O BaseDAO é uma classe base para gerenciar a sessão do banco de dados.

# Gerenciamento de Sessão: A classe gerencia a criação, o commit e o fechamento da sessão do banco de dados. 
# Isso é importante para garantir que as operações de banco de dados sejam realizadas corretamente e que os recursos sejam liberados após o uso.

# Context Manager: O uso de __enter__ e __exit__ permite que a classe seja usada com o operador with em Python, garantindo que os recursos sejam gerenciados automaticamente.

import logging
from models.db_credentials import get_session
from sqlalchemy.exc import IntegrityError, OperationalError, DataError

class BaseDAO(object):
    """
    A Base class for all managers. Automatically handles session creation,
    the commiting and closing the connections.
    """
    def __init__(self, session=None, commit_on_exit=True, close_on_exit=True):
        """
        Construtor da classe.

        :param session: Sessão do SQLAlchemy, se None, cria uma nova sessão.
        :param commit_on_exit: Booleano que indica se o commit deve ser feito automaticamente ao sair.
        :param close_on_exit: Booleano que indica se a sessão deve ser fechada automaticamente ao sair.
        """
        self._session = get_session() if (not session) else session
        self._commit_on_exit = commit_on_exit
        self._close_on_exit = close_on_exit

    def __enter__(self):
        """
        Método chamado ao entrar no contexto do 'with'.
        Retorna a própria instância (self), permitindo usar com 'with'.
        """
        return self

    def __exit__(self, *exc_info):
        """
        Método chamado ao sair do contexto do 'with'.

        :param exc_info: Informações da exceção, se houver.
        """
        if (self._session and self._commit_on_exit):
            try:
                # Tenta fazer o commit da sessão.
                self._session.commit()
            except IntegrityError as e:
                # Se ocorrer um erro de integridade, fecha a sessão e relança a exceção.
                self._session.close()
                raise e
            except OperationalError as e:
                # Trata erros operacionais, como perda de conexão.
                logging.error(f"Operational error: {e}")
                self._session.close()
                raise e
            except DataError as e:
                # Trata erros relacionados aos dados, como valores que excedem limites.
                logging.error(f"Data error: {e}")
                self._session.close()
                raise e
        if (self._session and self._close_on_exit):
                # Fecha a sessão ao sair, se necessário.
                self._session.close()

    def session(self):
        """
        Returns the session
        """
        return self._session
