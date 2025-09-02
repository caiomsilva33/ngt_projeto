# models.py

from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Aluno(Base):
    __tablename__ = "alunos"
    aluno_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    rg = Column(String(20))
    data_nascimento = Column(Date)
    idade = Column(Integer)
    instagram = Column(String(50))
    contato = Column(String(20))
    data_cadastro = Column(String)
    data_matricula = Column(Date)
    endereco_rua = Column(String(100))
    endereco_numero = Column(String(10))
    endereco_bairro = Column(String(50))
    endereco_cep = Column(String(10))
    nome_responsavel = Column(String(100))
    cpf_responsavel = Column(String(14))
    contato_responsavel = Column(String(20))
    instagram_responsavel = Column(String(50))
    foto_url = Column(String(255))

    usuario = relationship("Usuario", back_populates="aluno")
    matriculas = relationship("Matricula", back_populates="aluno")
    frequencias = relationship("Frequencia", back_populates="aluno")

class Usuario(Base):
    __tablename__ = "usuarios"
    usuario_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    cargo = Column(String(20), nullable=False)
    aluno_id = Column(Integer, ForeignKey("alunos.aluno_id"))

    aluno = relationship("Aluno", back_populates="usuario")

class Professor(Base):
    __tablename__ = "professores"
    professor_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    contato = Column(String(20))
    email = Column(String(100), unique=True, nullable=False)

class Pacote(Base):
    __tablename__ = "pacotes"
    pacote_id = Column(Integer, primary_key=True, index=True)
    nome_pacote = Column(String(50), nullable=False)
    modalidade = Column(String(50), nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    duracao_meses = Column(Integer, nullable=False)

class Matricula(Base):
    __tablename__ = "matriculas"
    matricula_id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.aluno_id"))
    pacote_id = Column(Integer, ForeignKey("pacotes.pacote_id"))
    horario_treino = Column(String(20), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_termino = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)

    aluno = relationship("Aluno", back_populates="matriculas")

class Frequencia(Base):
    __tablename__ = "frequencia"
    frequencia_id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.aluno_id"), nullable=False)
    data_presenca = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)

    aluno = relationship("Aluno", back_populates="frequencias")

class Pagamento(Base):
    __tablename__ = "pagamentos"
    pagamento_id = Column(Integer, primary_key=True, index=True)
    matricula_id = Column(Integer, ForeignKey("matriculas.matricula_id"))
    valor = Column(DECIMAL(10, 2), nullable=False)
    data_pagamento = Column(Date, nullable=False)
    metodo_pagamento = Column(String(50))
    status = Column(String(20), nullable=False)

class ProfessorAluno(Base):
    __tablename__ = "professor_aluno"
    professor_aluno_id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("professores.professor_id"), nullable=False)
    aluno_id = Column(Integer, ForeignKey("alunos.aluno_id"), nullable=False)