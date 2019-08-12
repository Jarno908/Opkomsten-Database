# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['E:\\Github\\Opkomsten-Database\\start_app.py'],
             pathex=['E:\\Github\\Opkomsten-Database', 'E:\\Github\\Opkomsten-Database'],
             binaries=[],
             datas=[('E:\\Github\\Opkomsten-Database\\Resources', 'Resources')],
             hiddenimports=[],
             hookspath=['c:\\python\\python36\\lib\\site-packages\\pyupdater\\hooks', 'E:\\Github\\Opkomsten-Database'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='win',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='E:\\Github\\Opkomsten-Database\\Resources\\app_icon_color.ico')
