import sqlite3


def decorator(banco):
    def inner(function):
        def commit_function(*args, **kwargs):
            """
            Decorator que comita as funções com os comandos sql.
            """
            connection = sqlite3.connect(banco)
            cursor = connection.cursor()
            args2 = function(*args, **kwargs)
            cursor.execute(*args2)
            retorno = cursor.fetchall()
            connection.commit()
            connection.close()
            return retorno
        return commit_function
    return inner


@decorator('spp.db')
def getLastId():
    """
    Função que retorna o último id do banco de dados.
    """
    return 'SELECT last_insert_rowid()',


@decorator('spp.db')
def create_table():
    """
    Função que verifica se existe a tabela dados, caso contrário,
    sera criada.
    """
    return ('CREATE TABLE IF NOT EXISTS dados (id INTEGER NOT NULL '
            'PRIMARY KEY, site TEXT, login TEXT, '
            'senha TEXT , sal TEXT)',)
    # AUTOINCREMENT coloca os id's para nunca repetir


@decorator('spp.db')
def data_entry(login='', senha='', sal='', site=''):
    """
    Função que adiciona dados pre definidos como site, login, senha,
    sal ao banco de dados.
    """
    return ('INSERT INTO dados (site, login, senha, sal) VALUES(?,?,?,?)',
            (site, login, senha, sal))


@decorator('spp.db')
def update_data(id, login='', senha='', sal='', site=''):
    """
    Função que atualiza os dados na tabela dados.
    """
    return ('UPDATE dados SET site=?, login=?, senha=?, sal=? ' +
            f'WHERE id = {id}', (site, login, senha, sal))


@decorator('spp.db')
def delete_data(id):
    """
    Função que deleta dados na tabela dados.
    """
    return f'DELETE FROM dados WHERE id = {id}',


# precisa procurar por login?
@decorator('spp.db')
def read_data(login=None, id=None):
    if id:
        return f'SELECT * FROM dados WHERE id = ?', (id,)
    elif login:
        return ('SELECT * FROM dados WHERE login LIKE' +
                f' "%{login}%" or site LIKE "%{login}%"',)
    else:
        return 'SELECT * FROM dados',
