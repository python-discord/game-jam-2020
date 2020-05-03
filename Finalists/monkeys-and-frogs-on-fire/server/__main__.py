from server.server import Server


def main():
    server = Server(__file__)
    server.run()


if __name__ == '__main__':
    main()
