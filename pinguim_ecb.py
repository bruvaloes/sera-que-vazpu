import sys
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PIL import Image, ImageDraw, ImageFont

TAM_BLOCO = 16  # AES trabalha com blocos de 16 bytes (128 bits)

IMAGEM_PADRAO = Path(__file__).parent / "imagens" / "foto.png"
PASTA_SAIDA = Path(__file__).parent / "resultados"


def carregar_imagem(caminho):
    if not caminho.exists():
        sys.exit(f"Imagem não encontrada: {caminho}\n"
                 "Coloque a foto em imagens/foto.png ou passe o caminho como argumento.")
    img = Image.open(caminho).convert("RGB")
    img.thumbnail((400, 400))  # mantém a demo rápida e o painel legível
    return img


def preparar(img):
    """Pixels crus (RGB) + padding com zeros até múltiplo de 16 bytes."""
    bruto = img.tobytes()
    return bruto + b"\x00" * (-len(bruto) % TAM_BLOCO)


def cifrar_ecb(dados, chave):
    return AES.new(chave, AES.MODE_ECB).encrypt(dados)


def cifrar_cbc(dados, chave):
    return AES.new(chave, AES.MODE_CBC, iv=get_random_bytes(16)).encrypt(dados)


def cifrar_ctr(dados, chave):
    return AES.new(chave, AES.MODE_CTR).encrypt(dados)


def para_imagem(dados, tamanho):
    n = tamanho[0] * tamanho[1] * 3
    return Image.frombytes("RGB", tamanho, dados[:n])


def blocos_repetidos(dados):
    """Total de blocos, blocos distintos e quantos aparecem mais de uma vez."""
    blocos = [dados[i:i + TAM_BLOCO] for i in range(0, len(dados), TAM_BLOCO)]
    distintos = len(set(blocos))
    return len(blocos), distintos, len(blocos) - distintos


def montar_painel(imagens, titulos, saida):
    w, h = imagens[0].size
    margem, topo = 10, 40
    painel = Image.new("RGB", (len(imagens) * (w + margem) + margem, h + topo + margem), "white")
    d = ImageDraw.Draw(painel)
    try:
        fonte = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
    except OSError:
        fonte = ImageFont.load_default()
    for i, (im, t) in enumerate(zip(imagens, titulos)):
        x = margem + i * (w + margem)
        painel.paste(im, (x, topo))
        d.text((x + 5, 8), t, fill="black", font=fonte)
    painel.save(saida)


def main():
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else IMAGEM_PADRAO
    img = carregar_imagem(caminho)
    PASTA_SAIDA.mkdir(exist_ok=True)

    chave = get_random_bytes(16)  # AES-128
    dados = preparar(img)

    resultados = {
        "ECB": cifrar_ecb(dados, chave),
        "CBC": cifrar_cbc(dados, chave),
        "CTR": cifrar_ctr(dados, chave),
    }

    print(f"Imagem {img.size[0]}x{img.size[1]} -> {len(dados)} bytes "
          f"= {len(dados) // TAM_BLOCO} blocos de 16 bytes\n")
    print(f"{'Modo':<6} {'blocos':>8} {'distintos':>10} {'repetidos':>10}")
    print("-" * 37)
    t, dist, rep = blocos_repetidos(dados)
    print(f"{'CLARO':<6} {t:>8} {dist:>10} {rep:>10}")

    imagens, titulos = [img], ["Original"]
    for modo, cifrado in resultados.items():
        im = para_imagem(cifrado, img.size)
        im.save(PASTA_SAIDA / f"{modo.lower()}.png")
        imagens.append(im)
        titulos.append(f"AES-{modo}")
        t, dist, rep = blocos_repetidos(cifrado)
        print(f"{modo:<6} {t:>8} {dist:>10} {rep:>10}")

    saida = PASTA_SAIDA / "painel.png"
    montar_painel(imagens, titulos, saida)
    print(f"\nPainel salvo em: {saida}")


if __name__ == "__main__":
    main()
