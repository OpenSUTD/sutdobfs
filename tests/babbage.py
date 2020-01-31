# from: http://www.rosettacode.org/wiki/Babbage_problem#Python


def main():
    print([x for x in range(30000) if (x * x) % 1000000 == 269696][0])


if __name__ == "__main__":
    main()
