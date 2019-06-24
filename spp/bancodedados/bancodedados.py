import sqlite3


def comitar(banco):
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


@comitar('spp.db')
def getLastId():
    """
    Função que retorna o último id da tabela dados do banco de dados.
    """
    return 'SELECT MAX(id) FROM dados',


@comitar('spp.db')
def create_table_dados():
    """
    Função que verifica se existe a tabela dados, caso contrário,
    será criada.
    """
    return ('CREATE TABLE IF NOT EXISTS dados (id INTEGER NOT NULL PRIMARY '
            'KEY AUTOINCREMENT, site TEXT, login TEXT, senha TEXT , sal TEXT)',)


@comitar('spp.db')
def create_table_admin():
    """
    Função que verifica se existe a tabela admin, caso contrário,
    será criada.
    """
    return ('CREATE TABLE IF NOT EXISTS admin (id INTEGER NOT NULL '
            'PRIMARY KEY, senha TEXT, sal TEXT)',)


@comitar('spp.db')
def data_entry(site='', login='', senha='', sal=''):
    """
    Função que adiciona dados pre definidos como site, login, senha,
    sal ao banco de dados.
    """
    return ('INSERT INTO dados (site, login, senha, sal) VALUES(?,?,?,?)',
            (site, login, senha, sal))


@comitar('spp.db')
def update_data(id, site='', login='', senha='', sal=''):
    """
    Função que atualiza os dados na tabela dados.
    """
    return ('UPDATE dados SET site=?, login=?, senha=?, sal=?'
            f' WHERE id = {id}', (site, login, senha, sal))


@comitar('spp.db')
def delete_data(id):
    """
    Função que deleta dados na tabela dados.
    """
    return f'DELETE FROM dados WHERE id = {id}',


@comitar('spp.db')
def delete_all_dados():
    return 'DELETE FROM dados WHERE id',


# precisa procurar por login?
# função não responsiva, refatorar?
@comitar('spp.db')
def read_data(login=None, id=None):
    if id:
        return f'SELECT * FROM dados WHERE id = {id}',
    elif login:
        return ('SELECT * FROM dados WHERE login LIKE'
                f' "%{login}%" or site LIKE "%{login}%"',)
    else:
        return 'SELECT * FROM dados',


@comitar('spp.db')
def adminUpdate(senha, sal):
    return (f'UPDATE admin SET senha = ?, sal = ? WHERE id = 1',
            (senha, sal))


@comitar('spp.db')
def adminInsert(senha, sal):
    return ('INSERT INTO admin (id, senha, sal) VALUES (?,?,?)',
            (1, senha, sal))


@comitar('spp.db')
def adminQuery():
    """
    Método que retorna senha e sal do programa.
    """
    return 'SELECT senha, sal FROM admin WHERE id = 1',
