import ftplib

host = 'ftp4.nska.net'
ftp_user = 'test1@lookies.by'
ftp_password = 'U4hq0oLn'
ftp = ftplib.FTP(host, ftp_user, ftp_password)
directory = ftp.nlst()
print(directory)