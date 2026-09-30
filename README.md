# Será Que Vazpu?

Este repositório contém a implementação prática desenvolvida para o seminário de Segurança Computacional. O projeto demonstra a metodologia de proteção e verificação de dados utilizada pelo site *Have I Been Pwned*, ilustrando como é possível consultar o vazamento de uma credencial sem expor ela durante o processo.

A base teórica e as técnicas criptográficas aplicadas neste código vêm dos capítulos estudados no livro didático da disciplina.

## Metodologia (K-Anonymity e SHA-1)

O sistema evita a exposição da senha combinando uma função de hash unidirecional (SHA-1) com o modelo de anonimato conhecido como *k-Anonymity*. O fluxo de verificação ocorre da seguinte forma:

1. **Processamento Local:** Não é seguro deixar a senha caminhando pelos programas em texto cru, então o script no lado do cliente aplica imediatamente a função SHA-1, transformando a senha em um código hexadecimal de 160 bits.
2. **Fragmentação:** O cliente divide esse hash e envia ao servidor apenas o prefixo (5 primeiros caracteres).
3. **Busca:** O servidor pesquisa esse prefixo em seu banco de dados de vazamentos e retorna uma lista contendo todos os sufixos (o restante do hash) associados àquele prefixo.
4. **Validação:** O cliente recebe a lista de sufixos e verifica, na própria máquina, se o seu sufixo original está entre os resultados retornados.

Com essa arquitetura, mesmo que a comunicação seja interceptada, o invasor terá acesso apenas a um fragmento de 5 caracteres, o que é insuficiente para reverter ou deduzir a senha original.

## Estrutura da Demonstração

A aplicação roda diretamente no terminal, sem a necessidade de bibliotecas externas. Usamos só os módulos nativos `hashlib`, `time` e `os` do Python. 

Para iniciar a demonstração, execute o comando:
```bash
python pwned.py
