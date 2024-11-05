def main():
    for i in range(7):
        s=" "*i+"*"*(7-i)
        print(s[:6-i]+"*"+s[7-i:])

if __name__ == '__main__':
    main()
    