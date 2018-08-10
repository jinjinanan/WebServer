import socket

HOST, PORT = '', 8888

# socket.AF_UNIX	用于同一台机器上的进程通信（既本机通信）
# socket.AF_INET	用于服务器与服务器之间的网络通信(指定使用IPv4)
# socket.AF_INET6	基于IPV6方式的服务器与服务器之间的网络通信
# socket.SOCK_STREAM	基于TCP的流式socket通信
# socket.SOCK_DGRAM	基于UDP的数据报式socket通信
# socket.SOCK_RAW	原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次SOCK_RAW也可以处理特殊的IPV4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头
# socket.SOCK_SEQPACKET	可靠的连续数据包服务

# 创建
# 绑定
# 监听
# 接受
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...' % PORT)

while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(request)

    http_response = b"""
    HTTP/1.1 200 OK

    Hello, World!
    """
    client_connection.sendall(http_response)
    client_connection.close()