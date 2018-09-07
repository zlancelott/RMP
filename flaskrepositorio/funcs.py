import os
from ftplib import FTP


def download_ftp_files():

    ftp = FTP('177.19.73.31')
    ftp.login(user='FTP_Server', passwd='ftpserver')

    ftp.cwd("/Computer Science/7-semester/Teoria da Computação/Aula 01/")

    filenames = ftp.nlst()

    for filename in filenames:
        # download the file
        local_filename = os.path.join(os.getcwd() + r"\flaskrepositorio\static\cache", filename)
        lf = open(local_filename, "wb")
        ftp.retrbinary("RETR " + filename, lf.write, 8 * 1024)
        lf.close()


def remove_files():
    ## APAGAR ARQUIVOS DEPOIS DO DOWNLOAD ##

    import os
    arq = os.listdir(os.getcwd() + r"\flaskrepositorio\static\cache")

    arq = [os.getcwd() + r"\flaskrepositorio\static\cache\\" + i for i in arq]

    for a in arq:
        os.remove(a)
