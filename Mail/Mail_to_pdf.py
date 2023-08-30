import imaplib
import email
from datetime import datetime
from email.header import decode_header
import os
import base64
import re

# 连接和登录imap
imap = imaplib.IMAP4_SSL('imap.feishu.cn', 993)
imap.login('zhangqian19826@yunexpress.cn', 'IxXqVL588YbytAFY')


# 选择文件夹LGG
imap.select('UKtaxBill')

# 搜索时间范围内的邮件
start = datetime(2023, 8, 29)
end = datetime(2023, 8, 30)
criteria = f'(SINCE {start.strftime("%d-%b-%Y")} BEFORE {end.strftime("%d-%b-%Y")})'
_, mails = imap.search(None, criteria)

for num in mails[0].split():
    # 获取邮件数据
    typ, data = imap.fetch(num, '(RFC822)')
    raw_email = data[0][1]
    # msg = email.message_from_bytes(data[0][1])

    msg = email.message_from_bytes(raw_email)


    # 递归获取正文
    def get_body(msg):
        if msg.is_multipart():
            parts = msg.get_payload()
            body = ""
            for part in parts:
                if isinstance(part, email.message.Message):
                    body += get_body(part)
                else:
                    body += part.get_payload()
            return body
        else:
            return msg.get_payload()


    body = get_body(msg)
    # print(body)
    decoded = base64.b64decode(body)
    # print(decoded)
    # 关闭连接

    pattern = rb'MAWB:\s(\d[-\d]*)'

    match = re.search(pattern, decoded)

    if match:
        s = match.group(1).decode()
        print(s)
    else:
        print("No match")

    folder_path = 'D:\\file\\' + s

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 遍历附件
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        # 获取编码后的文件名
        encoded_filename = part.get_filename()

        # 解码文件名
        decoded_filename = decode_header(encoded_filename)[0][0]
        file_encoding = decode_header(encoded_filename)[0][1]
        if file_encoding is not None:
            decoded_filename = decoded_filename.decode(file_encoding)

        # 下载附件
        attach_path = os.path.join(folder_path, decoded_filename)
        with open(attach_path, 'wb') as f:
            f.write(part.get_payload(decode=True))

        print("done 1")

print('附件下载完成!')
