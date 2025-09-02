# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, timedelta
from passlib.context import CryptContext
from typing import Optional
from . import models, schemas
from .database import engine, get_db

app = FastAPI()

# Cria todas as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# Configura o gerenciador de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Verifica se a senha em texto puro corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Cria um hash para a senha."""
    return pwd_context.hash(password)

def calcular_idade(data_nascimento: date) -> int:
    """Calcula a idade a partir da data de nascimento."""
    hoje = date.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

#--- API ENDPOINTS ---

@app.post("/alunos/cadastro", tags=["Cadastro"])
def create_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    """
    Endpoint para cadastrar um novo aluno.
    Também cria o usuário e a matrícula do aluno.
    """
    try:
        # 1. Verifica se o CPF já existe
        db_aluno_cpf = db.query(models.Aluno).filter(models.Aluno.cpf == aluno.cpf).first()
        if db_aluno_cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado.")

        # 2. Cria o registro do aluno
        idade_aluno = calcular_idade(aluno.data_nascimento)
        db_aluno = models.Aluno(
            nome=aluno.nome,
            email=aluno.email,
            cpf=aluno.cpf,
            rg=aluno.rg,
            data_nascimento=aluno.data_nascimento,
            idade=idade_aluno,
            instagram=aluno.instagram,
            contato=aluno.contato,
            data_matricula=aluno.data_matricula,
            endereco_rua=aluno.endereco_rua,
            endereco_numero=aluno.endereco_numero,
            endereco_bairro=aluno.endereco_bairro,
            endereco_cep=aluno.endereco_cep,
            nome_responsavel=aluno.nome_responsavel,
            cpf_responsavel=aluno.cpf_responsavel,
            contato_responsavel=aluno.contato_responsavel,
            instagram_responsavel=aluno.instagram_responsavel,
            foto_url=aluno.foto_url
        )
        db.add(db_aluno)
        db.commit()
        db.refresh(db_aluno)

        # 3. Cria o registro do usuário (login)
        hashed_password = get_password_hash(aluno.senha)
        db_usuario = models.Usuario(
            email=aluno.email,
            senha_hash=hashed_password,
            cargo="aluno", # Define o cargo como "aluno"
            aluno_id=db_aluno.aluno_id
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)

        # 4. Cria o registro de matrícula
        pacote = db.query(models.Pacote).filter(models.Pacote.pacote_id == aluno.pacote_id).first()
        data_termino = aluno.data_matricula + timedelta(days=pacote.duracao_meses * 30)

        db_matricula = models.Matricula(
            aluno_id=db_aluno.aluno_id,
            pacote_id=aluno.pacote_id,
            horario_treino=aluno.horario_treino,
            data_inicio=aluno.data_matricula,
            data_termino=data_termino,
            status="ativa" # Define o status inicial da matrícula
        )
        db.add(db_matricula)
        db.commit()
        db.refresh(db_matricula)

        # 5. Cria a relação entre professor e aluno
        db_relacao_prof_aluno = models.ProfessorAluno(
            professor_id=aluno.professor_id,
            aluno_id=db_aluno.aluno_id
        )
        db.add(db_relacao_prof_aluno)
        db.commit()

        return {"mensagem": "Aluno e matrícula cadastrados com sucesso!", "aluno_id": db_aluno.aluno_id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao cadastrar o aluno: {e}")