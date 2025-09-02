-- Tabela para armazenar as informações dos alunos
CREATE TABLE alunos (
    aluno_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    rg VARCHAR(20),
    data_nascimento DATE,
    idade INT,
    instagram VARCHAR(50),
    contato VARCHAR(20),
    data_cadastro TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    data_matricula DATE,
    endereco_rua VARCHAR(100),
    endereco_numero VARCHAR(10),
    endereco_bairro VARCHAR(50),
    endereco_cep VARCHAR(10),
    nome_responsavel VARCHAR(100),
    cpf_responsavel VARCHAR(14),
    contato_responsavel VARCHAR(20),
    instagram_responsavel VARCHAR(50),
    foto_url VARCHAR(255)
);

-- Tabela para armazenar usuários com diferentes níveis de acesso
-- Agora, a chave estrangeira aponta para 'aluno_id'
CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    cargo VARCHAR(20) NOT NULL,
    aluno_id INT NOT NULL,
    FOREIGN KEY (aluno_id) REFERENCES alunos(aluno_id) ON DELETE CASCADE
);

-- Tabela para gerenciar os professores
CREATE TABLE professores (
    professor_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    contato VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Tabela para ligar professores a alunos
CREATE TABLE professor_aluno (
    professor_aluno_id SERIAL PRIMARY KEY,
    professor_id INT NOT NULL,
    aluno_id INT NOT NULL,
    FOREIGN KEY (professor_id) REFERENCES professores(professor_id),
    FOREIGN KEY (aluno_id) REFERENCES alunos(aluno_id)
);

-- Tabela para gerenciar os pacotes e planos da academia
CREATE TABLE pacotes (
    pacote_id SERIAL PRIMARY KEY,
    nome_pacote VARCHAR(50) NOT NULL,
    modalidade VARCHAR(50) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    duracao_meses INT NOT NULL
);

-- Tabela para armazenar informações sobre matrículas
CREATE TABLE matriculas (
    matricula_id SERIAL PRIMARY KEY,
    aluno_id INT,
    pacote_id INT,
    horario_treino VARCHAR(20) NOT NULL,
    data_inicio DATE NOT NULL,
    data_termino DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (aluno_id) REFERENCES alunos(aluno_id),
    FOREIGN KEY (pacote_id) REFERENCES pacotes(pacote_id)
);

-- Tabela para registrar a frequência dos alunos
CREATE TABLE frequencia (
    frequencia_id SERIAL PRIMARY KEY,
    aluno_id INT NOT NULL,
    data_presenca DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (aluno_id) REFERENCES alunos(aluno_id)
);

-- Tabela para armazenar o histórico de pagamentos
CREATE TABLE pagamentos (
    pagamento_id SERIAL PRIMARY KEY,
    matricula_id INT,
    valor DECIMAL(10, 2) NOT NULL,
    data_pagamento DATE NOT NULL,
    metodo_pagamento VARCHAR(50),
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (matricula_id) REFERENCES matriculas(matricula_id)
);