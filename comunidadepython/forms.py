#aqui ficam todos os formulários do app.
#cada formulário é uma classe que comanda algum objeto do site. No flask já há boa parte da construção do formulário.
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadepython.models import Usuario
from flask_login import current_user
from wtforms import RadioField


class FormCriarConta(FlaskForm):
    usuario = StringField("Nome de Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 18)])
    confirmacao = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('O e-mail informado já pertence a outro usuário. Cadastre-se com outro e-mail ou faça login para continuar.')


class FormLogin(FlaskForm):
    email = StringField("E-mail",validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 18)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField("Fazer Login")


class FormEditarPerfil(FlaskForm):
    usuario = StringField("Nome de Usuário", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])]) #para que sejam utilizadas somente imagens e em formato PNG ou JPG.
    grau_escolar = RadioField(coerce=str, choices=['Curso/Certificação','Graduação', 'Pós-Graduação','Mestrado', 'Doutorado'])
    botao_submit_editarperfil = SubmitField("Confirmar Edição")

    def validate_email(self, email):
        if current_user.email != email.data: #para evitar que os usuários alterem o e-mail deles para um e-mail que já pertença a outro usuário.
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com este e-mail. Cadastre outro e-mail.')


class FormCriarPost(FlaskForm):
    titulo = StringField("Nome de Usuário", validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField("Criar Post")