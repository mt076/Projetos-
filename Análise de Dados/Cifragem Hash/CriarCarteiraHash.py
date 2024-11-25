import random
import hashlib

BIP39 = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd",
    "abuse", "access", "accident", "account", "accuse", "achieve", "acid", "acoustic", "acquire",
    "across", "act", "action", "actor", "actress", "actual", "adapt", "add", "addict", "address",
    "adjust", "admit", "adult", "advance", "advice", "aerobic", "affair", "afford", "afraid",
    "again", "age", "agent", "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
    "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone", "alpha", "already",
    "also", "alter", "always", "amateur", "amazing", "among", "amount", "amused", "analyst",
    "anchor", "ancient", "anger", "angle", "angry", "animal", "ankle", "announce", "annual",
    "another", "answer", "antenna", "antique", "anxiety", "any", "apart", "apology", "appear",
    "apple", "approve", "april", "arch", "arctic", "area", "arena", "argue", "arm", "armed",
    "armor", "army", "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact", "artist"
]

print("Pressione Enter para iniciar a criação da carteira BIP-39 de criptomoeda")
input()

carteira = random.sample(BIP39, 12)
palavras = " ".join(carteira)
hashMd5 = hashlib.md5(palavras.encode()).hexdigest()

print("Palavras da carteira gerada:", carteira)
print("Hash MD5 das palavras selecionadas:", hashMd5)
print("Carteira de criptomoeda criada com sucesso!")

print("Digite as palavras-chave da carteira para confirmar:")
Semente = input("Digite a semente de recuperação, separadas por espaço: ")


if len(Semente.split()) != 12:
    print("Erro: Digite somente as palavras de recuperação.")
else:

    hashmd5 = hashlib.md5(Semente.encode()).hexdigest()

    if hashmd5 == hashMd5:
        print("Parabéns. Carteira cripto recuperada com sucesso.")
    else:
        print("Está carteira cripto não existe.")
