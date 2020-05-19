from sys import argv
import Compiler as compiler

if len(argv) == 3:
    file = open(argv[1]).read()
    result, error = compiler.run(argv[1], file)
    if error: print(error.as_string())
    print(result)
    newfile = open(argv[2], "w")
    content = """
const {sahi, galat, khali, forcond,
  PUCHO, MATH_SQRT, LINE_LIKHO,
  MILAO, DALO, NIKAL, KYA_NUM,
  KYA_STR, KYA_LIST, LIKHO_WAPIS,
  JODH, LAMBAI, Value,
  RTError, Boolean, BasicInfinity,
  BasicString, BasicNumber, BasicArray,
  NullObject
} = require("./values.js")

/////////Generated Code//////////////////

"""
    content += result
    print(content)
    newfile.write(content)
    newfile.close()
else:
    while True:
        text = input("UrduBasicJs > ")
        result, error = compiler.run('<stdin>', text)
        if text.strip() == "": continue
        if error: print(error.as_string())
        print(result)
