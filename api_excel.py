from fastapi import FastAPI
import pandas as pd
from typing import List
from pydantic import BaseModel

app = FastAPI()

# 📖 Classe para receber novos itens (se quiser cadastrar)
class Produto(BaseModel):
    Produto: str
    Quantidade: int
    Valor_Unitario: float

# 🗂️ Rota principal: lê a planilha inteira
@app.get("/")
def read_estoque():
    df = pd.read_excel("estoque.xlsx")
    return df.to_dict(orient="records")

# 🔍 Filtrar por nome do produto
@app.get("/produto/{nome}")
def get_produto(nome: str):
    df = pd.read_excel("estoque.xlsx")
    resultado = df[df['Produto'].str.lower() == nome.lower()]
    return resultado.to_dict(orient="records")

# ➕ Adicionar um novo produto
@app.post("/adicionar")
def add_produto(produto: Produto):
    df = pd.read_excel("estoque.xlsx")
    novo = pd.DataFrame([produto.dict()])
    df = pd.concat([df, novo], ignore_index=True)
    df.to_excel("estoque.xlsx", index=False)
    return {"mensagem": "Produto adicionado com sucesso!"}

