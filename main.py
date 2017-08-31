import itchat
import api


@itchat.msg_register(itchat.content.TEXT)
def simple_reply(msg):
    if msg['ToUserName'] != 'filehelper':
        return

    if msg['Content'].strip().isdigit():
        view = api.find_bus_line_detail(msg['Content'].strip() + '路')
        itchat.send_msg(view, 'filehelper')
    else:
        itchat.send_msg('请输入要查询的线路数字\n(注意:快1输入b1)', 'filehelper')


def main():
    itchat.auto_login(hotReload=True)
    itchat.run()

if __name__ == "__main__":
    main()
