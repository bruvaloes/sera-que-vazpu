# AES: modos de operação (ECB, CBC e CTR)

Demonstração prática de por que **usar o AES não basta: o modo de operação faz
parte da segurança**. O script cifra uma imagem com AES-128 em três modos e
compara os resultados lado a lado.

> Trabalho desenvolvido para o seminário de criptografia da disciplina de
> Segurança Computacional, com base nos Capítulos 2, 20 e 21 de
> *Computer Security: Principles and Practice* (Stallings & Brown).

![Painel com a imagem original e o resultado em ECB, CBC e CTR](resultados/painel.png)

## O que a demonstração mostra

O AES cifra blocos de 128 bits (16 bytes). Para cifrar algo maior, é preciso
escolher **como** os blocos se combinam, e isso muda tudo:

| Modo | O que acontece | Resultado na imagem |
|------|----------------|---------------------|
| **ECB** | Cada bloco é cifrado sozinho | O contorno da imagem continua visível |
| **CBC** | Cada bloco depende do cifrado anterior | Ruído |
| **CTR** | O AES cifra um contador que mascara o texto | Ruído |

### Por que "pinguim ECB"?

O nome vem de um exemplo clássico: a imagem de um pinguim, o mascote do Linux,
cifrada com AES em ECB continua mostrando a silhueta do pinguim. Aqui repetimos
o experimento com uma imagem própria.

## Como cada modo funciona

- **ECB (Electronic Codebook):** `Ci = E(K, Pi)`. Blocos iguais no texto claro
  geram blocos iguais no cifrado, então o padrão da mensagem vaza.
- **CBC (Cipher Block Chaining):** `C0 = IV` e `Ci = E(K, Pi XOR Ci-1)`. O IV
  aleatório inicia a cadeia e cada bloco é misturado com o anterior, então
  blocos iguais deixam de gerar cifrados iguais.
- **CTR (Counter):** `Ci = Pi XOR E(K, nonce + i)`. O AES cifra um contador
  diferente para cada bloco e o resultado faz XOR com o texto. Funciona como
  cifra de fluxo, dispensa padding e pode ser paralelizado.

## Como executar

Requisitos: Python 3.8 ou superior.

```bash
# 1. Clone o repositório
git clone https://github.com/bruvaloes/aes-modos-de-operacao.git
cd aes-modos-de-operacao

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Rode a demonstração
python pinguim_ecb.py
```

O script lê a imagem em `imagens/foto.png`. Para usar outra, passe o caminho:

```bash
python pinguim_ecb.py caminho/da/imagem.png
```

### Qual imagem usar?

O efeito do ECB aparece melhor em imagens com **áreas grandes de cor lisa**:
logotipos, desenhos, camisetas, fundos limpos. Em fotos muito texturizadas,
quase não há blocos repetidos e o contorno some, mesmo no ECB. A imagem é
reduzida para no máximo 400x400 pixels para a demonstração ser rápida.

## O que o script produz

Na pasta `resultados/`:

- `ecb.png`, `cbc.png` e `ctr.png`: a imagem cifrada em cada modo;
- `painel.png`: a original e os três resultados lado a lado.

No terminal, uma tabela com a contagem de blocos de 16 bytes. O exemplo abaixo
é ilustrativo, e os valores mudam conforme a imagem:

```
Modo     blocos  distintos  repetidos
-------------------------------------
CLARO     30000        198      29802
ECB       30000        198      29802
CBC       30000      30000          0
CTR       30000      30000          0
```

**Como ler:** `repetidos = blocos - distintos`. No ECB, o texto cifrado tem
exatamente a mesma repetição do texto claro, e é isso que revela o padrão. No
CBC e no CTR, praticamente nenhum bloco se repete.

## Como o código funciona

1. Carrega a imagem, converte para RGB e reduz o tamanho.
2. Extrai os bytes dos pixels e completa com zeros até um múltiplo de 16 bytes.
3. Gera uma chave AES-128 aleatória, a mesma para os três modos.
4. Cifra os mesmos bytes em ECB, CBC (com IV aleatório) e CTR (com nonce aleatório).
5. Reconstrói uma imagem a partir de cada resultado e monta o painel.
6. Conta os blocos repetidos em cada saída.

Como a chave, o IV e o nonce são gerados a cada execução, as imagens em CBC e
CTR mudam de uma execução para outra, enquanto o contorno do ECB se mantém.

## Limitações e boas práticas

- **Sigilo não é integridade.** CBC e CTR escondem o conteúdo, mas não detectam
  alterações. Para isso existem o MAC e modos autenticados, como o GCM.
- **Nunca reutilize IV ou nonce com a mesma chave.** No CTR, repetir o nonce
  reaproveita a máscara e o XOR de dois cifrados revela o XOR dos textos claros.
- **Evite o ECB** para qualquer dado com estrutura ou repetição.
- Este código é **didático**. Ele cifra pixels crus sem cabeçalho e sem
  autenticação. Em sistemas reais, use bibliotecas e modos autenticados (AES-GCM).

## Estrutura do repositório

```
.
├── pinguim_ecb.py      # script da demonstração
├── requirements.txt    # dependências (pycryptodome, pillow)
├── imagens/
│   └── foto.png        # imagem usada na demonstração
└── resultados/         # imagens geradas pelo script
```

## Referências

- STALLINGS, W.; BROWN, L. *Computer Security: Principles and Practice*.
  4. ed. Pearson, 2017.
- DWORKIN, M. *Recommendation for Block Cipher Modes of Operation: Methods and
  Techniques*. NIST SP 800-38A, 2001.
- [Block cipher mode of operation (Wikipedia)](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)
