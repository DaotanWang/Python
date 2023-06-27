import win32com.client as win32

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = '111222@huawei.com'  #收件人
mail.CC = '111@huawei.com'  # 抄送人
#mail.Bcc='12345678@qq.com' #密抄收件人
mail.Subject = 'test1'  #邮件主题
# mail.Body = '这是一封测试邮件'  #邮件正文
mail.Importance = 1  #设置重要性为高
# mail.Attachments.Add(r'C:\Users\Desktop\测试.xlsx')  #添加附件
mail.HTMLBody  = '''
                    <table  border=1>
	                <caption>media list</caption>
	                <tr>
                      <td>PH Phones-Only includes TOP media - Tier 1&2</td>
                      <td><a class="btn btn-primary" href="https://twitter.com/i/lists/1614818322805313536?s=20">Click Me!</a></td>
                    </tr>
                    <tr>
                      <td>TH Phones -Only includes TOP media - Tier 1&2</td>
                      <td><a class="btn btn-primary" href="https://twitter.com/i/lists/1614818322805313536?s=20">Click Me!</a></td>
                    </tr>
                    <tr>
                      <td>MY Phones -Only includes TOP media - Tier 1&2</td>
                      <td><a class="btn btn-primary" href="https://twitter.com/i/lists/1614818322805313536?s=20">Click Me!</a></td>
                    </tr>
                    
                    </table>
                 '''
mail.Send()   #发送
