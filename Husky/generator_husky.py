def gen(x):
    for i in range(x):
        yield i


g = gen(10)

if __name__ == '__main__':
    print(next(g))
    print(next(g))

    # print vars(g)
    # bytes = wrap.dumps(g)
    # print g.next()
    # g2 = wrap.loads(bytes)
    # print g2.next()

    # print help(types.GeneratorType)
    print(type(g))
