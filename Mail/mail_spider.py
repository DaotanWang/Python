import imaplib
import email
import re
from pygtrans import Translate
import datetime
from translate import Translator
import openpyxl

def format_date1(user_date):
  date = datetime.datetime.strptime(user_date, '%Y.%m.%d')
  return date.strftime('%d-%b-%Y')

def format_date2(user_date):
  date = datetime.datetime.strptime(user_date, '%Y.%m.%d')
  return date.strftime('%d-%b-%Y')

print('请输入开始日期(格式:YYYY.MM.DD):')
start_date = input()
start_date = format_date1(start_date)

print('请输入结束日期(格式:YYYY.MM.DD):')
end_date = input()
end_date = format_date2(end_date)

client = Translate()
username = 'ssd-cjzc@yunexpress.cn'
password = 'hxxxxxxxxx'
# 连接到IMAP服务器
mail = imaplib.IMAP4_SSL('imap.feishu.cn', 993)
# 登录邮箱
mail.login(username, password)
# 选择收件箱
mail.select('INBOX')
# 搜索条件,发件人和日期范围
search_criteria = f'(SINCE {start_date} BEFORE {end_date})'
# 搜索邮件
typ, data = mail.search(None, search_criteria)

wb = openpyxl.Workbook()
sheet = wb.active
sheet['A1'] = '单号'
sheet['B1'] = '正文'
sheet['C1'] = '译文'
n = 0
# 遍历邮件编号
for num in data[0].split():
    # 获取邮件内容
    typ, msg_data = mail.fetch(num, '(RFC822)')
    # 解析邮件
    email_msg = email.message_from_bytes(msg_data[0][1])
    # from_email = email_msg['From']
    # from_name = decode_header(from_email)[0][0]
    from_email = email_msg['From']
    start = from_email.find('<') + 1
    end = from_email.find('>')
    from_address = from_email[start:end]
    # 打印邮件正文
    if email_msg.is_multipart():
        body = ''
        for part in email_msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload()
    else:
        body = email_msg.get_payload()
    print("loading")
    if from_address == 'HermesCustomerServices@hermes-europe.co.uk':
        # print(f'From!!!!!!!!!!!!!!!!!!!!: {from_address}')
        # print(f'Message!!!!!!!!!!!!!!!!!: \n{body}')
        body = re.sub("=", "", body)
        text = client.translate(body)
        results = text.translatedText

        pattern = r'Evri email enquiry (.*)'
        match = re.search(pattern, body)
        if match:
            ID = match.group(1)
            try:
                cell1 = 'A' + str(n + 2)
                sheet[cell1] = str(ID)
                cell2 = 'B' + str(n + 2)
                sheet[cell2] = str(body)
                cell3 = 'C' + str(n + 2)
                sheet[cell3] = str(results)
            except BaseException:
                pass
            n = n + 1


        print('-' * 50)
    else:
        pass

wb.save(r'D:\\file\\Hermes.xlsx')
# 关闭连接
mail.close()
mail.logout()

