# Benchmarking de Embeddings Jurídicos em Português

Este repositório contém o código-fonte e os notebooks utilizados no artigo:

**"Benchmarking de Embeddings Jurídicos em Português: Uma Análise Semântica de Ementas do TRT-23"**  
Autor: *Marjory Salles Soehn Lima*  
Afiliação: Mestrado em Computação Aplicada - UFMT

## 📚 Descrição

O objetivo deste projeto é realizar um benchmarking de diferentes modelos de embeddings em língua portuguesa aplicados ao domínio jurídico, por meio de agrupamento semântico de ementas extraídas do Tribunal Regional do Trabalho da 23ª Região (TRT‑23). São avaliados os modelos FastText, Doc2Vec, SBERT, BERTimbau e LegalBERT-pt com o algoritmo HDBSCAN e extração de termos por TF-IDF.

## 📁 Estrutura do Repositório

```
.
├── notebooks/
│   └── benchmarking_experimentos.ipynb       # Notebook principal com os experimentos
│
├── scripts/
│   ├── scraper_trt23.py                      # Script de extração de ementas via web
│
├── data/
│   └── ementas.zip                           # Conjunto de dados extraído via web
│
├── results/
│   ├── graficos/                             # Imagens e visualizações geradas nos experimentos
│   ├── Tabelas/                              # Tabelas geradas nos experimentos
│   └── clusters_amostrados.csv               # Exemplo de saída dos clusters
│
├── requirements.txt                          # Dependências do projeto (Python >= 3.8)
├── LICENSE                                   # Licença aberta (MIT)
└── README.md
```

## 🧪 Modelos Avaliados

- `FastText` 
- `Doc2Vec`
- `SBERT` (`paraphrase-multilingual-mpnet-base-v2`)
- `BERTimbau` (`neuralmind/bert-base-portuguese-cased`)
- `LegalBERT-pt` (`raquelsilveira/legalbertpt_fp`)

## 🛠️ Como Reproduzir

1. Clone o repositório:

```bash
git clone https://github.com/msoehn3/benchmarking-embeddings-juridicos.git
cd benchmarking-embeddings-juridicos
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o notebook principal:

Abra o Jupyter Notebook e carregue:
```bash
notebooks/benchmarking_experimentos.ipynb
```

## 📌 Citação

Se este código for útil para sua pesquisa, por favor cite da seguinte forma:

```bibtex
@misc{msoehn32025benchmarking,
  author = {Marjory Salles Soehn Lima},
  title = {Benchmarking de Embeddings Jurídicos em Português},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/msoehn3/benchmarking-embeddings-juridicos}}
}
```

## ⚖️ Licença

Este projeto é distribuído sob a licença [MIT](LICENSE).
