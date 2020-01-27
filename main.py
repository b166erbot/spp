#!/usr/bin/python3
from spp.spp import main
from os import chdir
from pathlib import Path

if __name__ == '__main__':
    local_deste_arquivo = Path(__file__).parent
    chdir(local_deste_arquivo)
    main()
