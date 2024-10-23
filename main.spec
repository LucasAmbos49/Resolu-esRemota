# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # Seu arquivo principal
    pathex=['C:\\caminho\\para\\CADI Master BLUEGEM INFINITAAAA'],  # O caminho onde está o seu projeto
    binaries=[],
    datas=[
        ('modules', 'modules'),   # Inclui a pasta 'modules' com todos os arquivos e subpastas
        ('bats', 'bats'),         # Inclui a pasta 'bats' com todos os arquivos
	('Install_printer', 'Install_printer'),         # Inclui a pasta 'bats' com todos os arquivos
        ('logs', 'logs'),         # Inclui a pasta 'logs'
        ('programas.json', '.'),  # Inclui o arquivo JSON 'programas.json' na raiz
        ('install_program.bat', '.'),  # Inclui o instalador bat na raiz
        ('teste.bat', '.'),  # Inclui o arquivo 'teste.bat'
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Use False se não quiser abrir um console junto
	 icon='logo.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)
