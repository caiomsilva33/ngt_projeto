# schemas.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

# Schema para o cadastro completo de um novo aluno
class AlunoCreate(BaseModel):
    # Dados pessoais
    nome: str
    email: str
    senha: str
    cpf: str
    rg: Optional[str] = None
    data_nascimento: date
    instagram: Optional[str] = None
    contato: Optional[str] = None

    # Endereço
    endereco_rua: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cep: Optional[str] = None

    # Dados do responsável
    nome_responsavel: Optional[str] = None
    cpf_responsavel: Optional[str] = None
    contato_responsavel: Optional[str] = None
    instagram_responsavel: Optional[str] = None

    # Dados da matrícula
    horario_treino: str
    data_matricula: date
    pacote_id: int
    professor_id: int

    # URL da foto
    foto_url: Optional[str] = None