def describe(df, title):
    print("______________________________________________________")

    print("{}: \n".format(title))
    print("Head des Datensatzes:")
    print(df.head(2))
    print("\n")
    print("Describe:")
    print(df.describe())
    print("\n")
    print("Info:")
    print(df.info())
    print("\n")
    print("______________________________________________________")
