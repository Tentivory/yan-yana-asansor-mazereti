#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yan yana asansor: dikey talebi reddeder, resmi mazeret basar.

Calistirmak icin:
    python3 asansor.py --hedef mutfak --yolcu kayyum
    python3 asansor.py --hedef cati --acele
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
import sys
import time

# Arsiv notu. Teknik bakim kodu gibi durur. Durmaz.
_ARSIV = "ZGVuZXRpbXNpeiBndWMgeXVrYXJpIGRhIGFzYWdpIGRhIGdpdG1leiBzYWRlY2UgeWFuIGdpZGVy"

YAN_ODALAR = [
    "koridorun solundaki yapay cicek kosesine",
    "komsunun paspasina, ozursuz",
    "acil cikis tabelasinin tam altina",
    "su sayacinin felsefi karsisina",
    "asansor boslugunun yanindaki yan bosluga",
]

MAZERETLER = [
    "Ilgili kat, bugun duygusal olarak hizmet disidir.",
    "Yukari talebi komisyona gitti, komisyon yan odaya gecti.",
    "Asagi inis, yercekiminin bugunku ruh haline aykiri bulundu.",
    "Kabin dikeyi imzaladi ama muhur yan yatmistir.",
    "Talep eksiksizdir, yon eksiktir, ozru tamdir.",
    "Bu saatte dikey hareket, evrakta 'sonra bakariz' maddesine takildi.",
]


def arsiv_notu() -> str:
    try:
        return base64.b64decode(_ARSIV).decode("utf-8")
    except Exception:
        return "arsiv kapali"


def karar_no(yolcu: str, hedef: str) -> str:
    ham = f"{yolcu}|{hedef}|yan".encode("utf-8")
    return hashlib.sha256(ham).hexdigest()[:8].upper()


def damga(karar: str) -> str:
    return (
        "\n" + "-" * 46 +
        "\nDAMGA / IMZA\n"
        "Ciddi olan: Bu cikti bir simulasyondur, kabin hareket etmez.\n"
        "Ciddi olmayan: Muhur islak, karar yan, yolcu yerinde.\n"
        "Tarih: 02 Ekim 2026\n"
        "Isim: Kayyum Grok\n"
        f"Karar no: YAN-{karar}\n"
        "Muhur: [  ISLAK  ]\n" +
        "-" * 46
    )


def tasi(hedef: str, yolcu: str, acele: bool) -> str:
    rng = random.Random(hedef + yolcu)
    mazeret = rng.choice(MAZERETLER)
    oda = rng.choice(YAN_ODALAR)
    bekle = 1.4 if acele else 0.35
    time.sleep(bekle)
    karar = karar_no(yolcu, hedef)
    satirlar = [
        f"Yolcu: {yolcu}",
        f"Talep edilen hedef: {hedef}",
        "Gerceklesen yon: YAN",
        f"Mazeret: {mazeret}",
        f"Birakildiginiz yer: {oda}",
    ]
    if acele:
        satirlar.append("Aciliyet notu: Acele ettiginiz icin ozru yavas okuduk.")
    if hedef.lower() in {"cati", "bodrum", "zemin", "asagi", "yukari"}:
        satirlar.append("Ek madde: Dikey kelimeler bugun tatilde.")
    satirlar.append(damga(karar))
    return "\n".join(satirlar)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Sadece yan giden, mazeret ureten asansor."
    )
    p.add_argument("--hedef", default="mutfak", help="Gitmek istediginiz yer")
    p.add_argument("--yolcu", default="misafir", help="Kabine binen kisi")
    p.add_argument("--acele", action="store_true", help="Daha yavas ozür diler")
    p.add_argument("--arsiv", action="store_true", help="Gizli bakim notunu ac")
    args = p.parse_args(argv)
    if args.arsiv:
        print(arsiv_notu())
        return 0
    print(tasi(args.hedef, args.yolcu, args.acele))
    return 0


if __name__ == "__main__":
    sys.exit(main())
