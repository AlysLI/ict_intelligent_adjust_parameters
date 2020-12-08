# -*- coding: utf-8 -*-
import pysftp
import os


def SynData(GUI_class, program_name):
    sHostName = '192.168.200.188'
    sUserName = 'ict'
    sPassWord = 'ict'

    # cnopts = pysftp.CnOpts(knownhosts='known_hosts')
    # cnopts.hostkeys = None
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    DB_has_data = False
    PC_has_data = False

    with pysftp.Connection(sHostName,
                           username=sUserName,
                           password=sPassWord,
                           cnopts=cnopts) as sftp:
        # 判斷 IAI base是否存在,並進入IAI database目錄
        if sftp.isdir('IAI_database'):
            sftp.cwd('./IAI_database/')
        else:
            sftp.makedirs('IAI_database')
            sftp.cwd('./IAI_database/')

        # 判斷程式是否已經在DB存在
        if sftp.isdir(program_name):
            DB_has_data = True
            print('DB has had data already...')
        else:
            DB_has_data = False
            print("DB hasn\'t had data...")

        # 判斷程式是否已經在PC存在
        if os.path.exists('C:\\IAI_AI' + '\\' + program_name):
            PC_has_data = True
            print('PC has had data already...')
        else:
            PC_has_data = False
            print("PC hasn\'t had data...")

        # 未來可以加入spec檔，確認資料沒有遺漏、被刪除等情況
        local = 'C:\\IAI_AI\\' + program_name + '\\'
        remote = '/IAI_database/' + program_name + '/'

        # 如果DB不存在，PC存在，上傳所有PC資料
        if PC_has_data and not DB_has_data:
            sftp.makedirs(program_name)
            sftp.cwd(program_name)
            if os.path.isdir(local):
                for f in os.listdir(local):
                    if os.path.isfile(local + f):
                        # 上传目录中的文件
                        sftp.put(os.path.join(local+f), os.path.join(f))
                    elif os.path.isdir(local + f):
                        sftp.mkdir(f)
                        sftp.cwd(f)
                        for f2 in os.listdir(local + f):
                            # 上传目录中的文件
                            sftp.put(os.path.join(local + f + '\\' + f2), os.path.join(f2))
                        sftp.cwd("..")
        # 如果DB存在，PC不存在，下載所有DB資料
        elif not PC_has_data and DB_has_data:
            os.mkdir(local)
            os.chdir(local)
            if sftp.isdir(remote):
                for f in sftp.listdir(remote):
                    if sftp.isfile(remote + f):
                        # 下載目录中的文件
                        sftp.get(os.path.join(remote + f), os.path.join(f))
                    elif sftp.isdir(remote + f):
                        os.mkdir(f)
                        os.chdir(f)
                        print(os.getcwd())
                        for f2 in sftp.listdir(remote + f):
                            sftp.get(os.path.join(remote + f + '/' + f2), os.path.join(f2))  # 下載目录中的文件
                        os.chdir("..")
        # 如果DB不存在，PC不存在，則pass
        elif not PC_has_data and not DB_has_data:
            pass
        # 如果都存在，同步parameter_save
        elif PC_has_data and DB_has_data:
            pass

        '''
            sftp.makedirs(program_name)
            sftp.cwd('./' + program_name + '/')
            sftp.put('C:\\IAI_AI\\' + program_name + '\\step_data.xlsx',
                     preserve_mtime = True)
            sftp.put('C:\\IAI_AI\\' + program_name + '\\Device_data.xlsx',
                     preserve_mtime = True)
        '''

        # 取得目錄內容
        directory = sftp.listdir_attr()

        # 印出結果
        for attr in directory:
            print(attr.filename)

        sftp.close()
