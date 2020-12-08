<<<<<<< HEAD
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['ict\\testlogic\\ICT_Testing_Mode.py', 'ict\\testlogic\\R_mode_learning.py', 'ict\\testlogic\\C_mode_learning.py', 'ict\\testlogic\\D_mode_learning.py', 'ict\\testlogic\\J_mode_learning.py', 'ict\\db_func\\ICT_syn_data.py', 'ict\\rpa\\ICT_RPA.py', 'ict\\gui\\ICT_GUI.py', 'ict\\dataprocessing\\ICT_GetData.py', 'common\\ICT_general_function.py', 'C:\\Users\\henry\\Desktop\\ict_intelligent_adjust_parameters'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          [],
          exclude_binaries=True,
          name='ICT_smart_turning',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='pics\\ICT.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ICT_smart_turning')
=======
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['ict\\testlogic\\ICT_Testing_Mode.py', 'ict\\testlogic\\R_mode_learning.py', 'ict\\testlogic\\C_mode_learning.py', 'ict\\testlogic\\D_mode_learning.py', 'ict\\testlogic\\J_mode_learning.py', 'ict\\db_func\\ICT_syn_data.py', 'ict\\rpa\\ICT_RPA.py', 'ict\\gui\\ICT_GUI.py', 'ict\\dataprocessing\\ICT_GetData.py', 'common\\ICT_general_function.py', 'C:\\Users\\henry\\Desktop\\ict_intelligent_adjust_parameters'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          [],
          exclude_binaries=True,
          name='ICT_smart_turning',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='pics\\ICT.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ICT_smart_turning')
>>>>>>> b836e0ccff4ea304c4967c9bd5daca4be6311525
