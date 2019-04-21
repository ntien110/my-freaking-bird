def getResult(generation):
    file =open('generations/gen_[{0}].txt'.format(generation),'r')
    raw=file.readline()
    all=''
    while raw:
        raw=raw.replace(chr(10),'')
        raw=raw.replace(' '*7,'')
        raw = raw.replace( '[[array' ,chr(10)+'[[array')
        all+=raw
        raw=file.readline()
    file.close()
    print( all)
getResult(113)
