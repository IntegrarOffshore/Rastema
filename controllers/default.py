# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use # @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

# def mylogin():
#     return dict(form=auth.login())
# def myregister():
#     return dict(form=auth.register())
# def myprofile():
#     return dict(form=auth.profile())

def ver_usuarios():
    grid = SQLFORM.grid(db.auth_user)
    return dict(grid=grid)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def index():
    return dict()

# @auth.requires_login()
def level():
    return dict()

# Página de suporte
def suporte():
    return dict()

# Página de testes
def teste():
    if request.vars.filme:
        session.flash = request.vars.teste
    return dict()


# --------------------------------------------------------------------FORNECEDOR

# @auth.requires_login()
def cadastro_fornecedor():
    form = SQLFORM(Fornecedor)
    if form.process().accepted:
        session.flash = 'Novo Fornecedor: %s' % form.vars.nome
        redirect(URL('cadastro_fornecedor'))
    elif form.errors:
        response.flash = 'Erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário'
    return dict(form=form)

# @auth.requires_login()
def ver_fornecedor():
    if 'edit' in request.args:
        edit = request.args
        response.flash = edit
        parametro = edit[2]
        url = 'editar_fornecedor/' + parametro
        redirect(URL(url))
    if 'view' in request.args:
        # db.fornecedor.id.readable = False # or writable
        view = request.args
        response.flash = view
        parametro = view[2]
        url = 'fornecedor_details/' + str(parametro)
        redirect(URL(url))
    grid = SQLFORM.grid(Fornecedor, create=False, advanced_search = False,
    fields=[db.fornecedor.cnpj,
            db.fornecedor.nome,
            db.fornecedor.inscricao_estadual,
            db.fornecedor.telefone,
            db.fornecedor.email],
            maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

# @auth.requires_login()
def editar_fornecedor():
    db.fornecedor.id.readable = False
    form = SQLFORM(Fornecedor, request.args(0, cast=int))
    if form.process().accepted:
        session.flash = 'Fornecedor atualizado: %s' % form.vars.nome
        redirect(URL('ver_fornecedor'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Atualização de dados'
    return dict(form=form)

# Ver detalhes dos fornecedores

def fornecedor_details():
    '''
    Aqui o request.arg (0) pega o parametro URL e executa o select no banco de
    dados "http://0.0.0.0/Rastema/default/fornecedor_details/09477210000140"
    '''
    fornecedor_details = db(Fornecedor.id == request.args(0)).select()
    return dict(fornecedor_details=fornecedor_details)




# ------------------------------------------------------------------EQUIPAMENTOS

def cadastro_equipamento():
    form = SQLFORM(Equipamento)
    # db.executesql("SET FOREIGN_KEY_CHECKS = 0;")
    if form.process().accepted:
        session.flash = 'Novo Equipamento: %s' % (form.vars.descricao)
        redirect(URL('cadastro_equipamento'))
        # db.executesql("SET FOREIGN_KEY_CHECKS = 1;")
    elif form.errors:
        response.flash = 'Erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = ''
    return dict(form=form)

def ver_equipamento():
    if 'edit' in request.args:
        edit = request.args
        response.flash = edit
        parametro = edit[2]
        url = 'editar_equipamento/' + parametro
        redirect(URL(url))
    if 'view' in request.args:
        view = request.args
        response.flash = view
        parametro = view[2]
        url = 'equipamento_details/%s' % (parametro)
        redirect(URL(url))
    grid = SQLFORM.grid(Equipamento, create=False, advanced_search = False,
    fields=[db.equipamento.fornecedor,
            db.equipamento.descricao,
            db.equipamento.tag,
            db.equipamento.ax_cod],
            maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

def editar_equipamento():
    db.equipamento.id.readable = False
    db.equipamento.fornecedor.writable = False
    db.equipamento.fornecedor.readable = False
    form = SQLFORM(Equipamento, request.args(0, cast=str))
    if form.process().accepted:
        session.flash = 'Equipamento atualizado: %s' % form.vars.descricao
        redirect(URL('ver_equipamento'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Atualização de dados'
    return dict(form=form)

def equipamento_details():
    equipamento_details = db(Equipamento.id == request.args(0)).select()
    return dict(equipamento_details=equipamento_details)




# -------------------------------------------------------LOCAÇÃO DE EQUIPAMENTOS
# def selecione_fornecedor():
#     fornecedor_select = db(db.fornecedor.id > 0).select()
#     selecione_fornecedor = request.args(0)
#     return dict(fornecedor_select=fornecedor_select)


def cadastro_pedido():
    form = SQLFORM(Pedido)
    if form.process().accepted:
        session.flash = 'Novo pedido cadastrado'
        redirect(URL(''))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Atualização de dados'
    return dict(form=form)

def ver_pedido():
    if 'edit' in request.args:
        edit = request.args
        response.flash = edit
        parametro = edit[2]
        url = 'editar_pedido/' + parametro
        redirect(URL(url))
    if 'view' in request.args:
        view = request.args
        response.flash = view
        parametro = view[2]
        url = 'pedido_details/%s' % (parametro)
        redirect(URL(url))
    grid = SQLFORM.grid(Pedido, create=False, advanced_search = False,
    fields=[db.pedido.id,
            db.pedido.equipamento,
            db.pedido.plataforma,
            db.pedido.data_prevista_fim,
            db.pedido.valor,
            db.pedido.created_on
            ],
            maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

def editar_pedido():
    # db.equipamento.id.readable = False
    # db.equipamento.fornecedor.writable = False
    # db.equipamento.fornecedor.readable = False
    form = SQLFORM(Equipamento, request.args(0, cast=int))
    if form.process().accepted:
        session.flash = 'Equipamento atualizado: %s' % form.vars.descricao
        redirect(URL('ver_equipamento'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Atualização de dados'
    return dict(form=form)












#
# def cadastro_pedido():
#     form = SQLFORM(Fornecedor_Equipamento)
#     cont = 0
#     if form.process().accepted:
#         quantidade = request.vars.quantidade
#         quantidade = int(quantidade)
#
#         while quantidade > 1:
#             db.fornecedor_equipamento.insert(fornecedor=form.vars.fornecedor,
#                                              equipamento=form.vars.equipamento,
#                                              valor=form.vars.valor,
#                                              data_pedido = form.vars.data_pedido,
#                                              data_prevista_fim = form.vars.data_prevista_fim
#                                              )
#             quantidade = quantidade - 1
#         session.flash = 'Pedido Realizado'
#         for row in db(db.equipamento.ax_cod == form.vars.equipamento).select():
#             eqpt_select = row
#         for row in db(db.fornecedor.cnpj == form.vars.fornecedor).select():
#             forn_select = row
#         db(db.fornecedor_equipamento.equipamento == form.vars.equipamento).update(equipamento_nome=eqpt_select.detalhe)
#         db(db.fornecedor_equipamento.fornecedor == form.vars.fornecedor).update(fornecedor_nome=forn_select.nome)
#         redirect(URL('cadastro_pedido'))
#     elif form.errors:
#         response.flash = 'Erros encontrados no formulário'
#     else:
#         if not response.flash:
#             response.flash = ''
#     return dict(form=form)
#
# def almoxarife():
#     form = SQLFORM(Almoxarife)
#     if form.process().accepted:
#         for row in db(db.fornecedor_equipamento.id == form.vars.fornecedor_equipamento).select():
#             loca_select = row
#         # Cadastrar valores na mesma tabela que recebe. O produto deixa de ser um pedido
#         db(db.almoxarife.id == form.vars.id).update(fornecedor=loca_select.fornecedor,
#                                                     equipamento = loca_select.equipamento,
#                                                     fornecedor_nome = loca_select.fornecedor_nome,
#                                                     equipamento_nome = loca_select.equipamento_nome,
#                                                     valor = loca_select.valor,
#                                                     data_pedido = loca_select.data_pedido,
#                                                     status = 'Almoxarifado'
#                                                     )
#         # Remover o pedido, agora se torna um equipamento
#         db(db.fornecedor_equipamento.id == form.vars.fornecedor_equipamento).delete()
#         session.flash = 'teste'
#         redirect(URL('almoxarife'))
#     elif form.errors:
#         response.flash = 'Erros encontrados no formulário'
#     else:
#         if not response.flash:
#             response.flash = ''
#     return dict(form=form)


# READ

# def ver_fornecedor():
#     grid = SQLFORM.grid(Fornecedor,
#     fields =[db.fornecedor.cnpj,
#              db.fornecedor.nome,
#              db.fornecedor.telefone,
#              db.fornecedor.email],
#     maxtextlength=16,
#     exportclasses=dict(tsv_with_hidden_cols=False,
#                        csv=False, xml=False, json=False))
#     return dict(grid=grid)
#
# def ver_equipamento():
#     if 'edit' in request.args:
#         edit = request.args
#         response.flash = edit
#         param = edit[2]
#         url = 'editar_equipamento/' + param
#         redirect(URL(url))
#     grid = SQLFORM.grid(Equipamento,
#     fields=[db.equipamento.nome,
#             db.equipamento.descricao,
#             db.equipamento.ax_cod],
#
#             maxtextlength=16,
#
#     exportclasses=dict(tsv_with_hidden_cols=False,
#                        csv=False, xml=False, json=False))
#     return dict(grid=grid)
#
# def ver_locacao():
#     grid = SQLFORM.grid(Fornecedor_Equipamento,
#
#     fields=[db.fornecedor_equipamento.fornecedor,
#             db.fornecedor_equipamento.equipamento,
#             db.fornecedor_equipamento.valor,
#             db.fornecedor_equipamento.data_pedido,
#             db.fornecedor_equipamento.data_prevista_fim],
#
#     maxtextlength=25,
#
#     exportclasses=dict(tsv_with_hidden_cols=False,
#                        csv=False,xml=False,json=False))
#
#     return dict(grid=grid)
#
# def ver_almoxarife():
#     if 'view' in request.args:
#         db.almoxarife.fornecedor_equipamento.readable = False # or writable
#         db.almoxarife.id.readable = False
#         db.almoxarife.equipamento.readable = False
#         db.almoxarife.fornecedor.readable = False
#
#     grid = SQLFORM.grid(Almoxarife,
#     fields=[db.almoxarife.equipamento_nome,
#             db.almoxarife.fornecedor_nome,
#             db.almoxarife.tag,
#             db.almoxarife.plataforma,
#             db.almoxarife.data_recebida,
#             db.almoxarife.status],
#     maxtextlength=25,
#     exportclasses=dict(tsv_with_hidden_cols=False,
#                        csv=False,xml=False,json=False))
#
#
#
#     return dict(grid=grid)
#
#
# # UPDATE
#
# '''Os argumentos de uma URL são guardados no formato de uma lista, por isso,
#    para recebermos o valor de um argumento específico, devemos passar o índice
#    desse argumento na lista. Por exemplo: request.args(0) vai pegar o primeiro
#    elemento da lista.Além disso, o request.args() tem um parâmetro opcional
#    chamado cast para especificar o tipo de retorno que você deseja ter.
#    Por padrão, todos os argumentos estão em formato de string'''
#
# def editar_equipamento():
#     form = SQLFORM(Equipamento, request.args(0, cast=int))
#     if form.process().accepted:
#         session.flash = 'Equipamento atualizado: %s' % form.vars.nome
#         redirect(URL('ver_equipamento'))
#     elif form.errors:
#         response.flash = 'Erros no formulário!'
#     else:
#         if not response.flash:
#             response.flash = 'Preencha o formulário!'
#     return dict(form=form)
