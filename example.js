
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

function oopify(prefix) {	
	return (prefix.copy().added_to(new BasicString("oop")))
	
};
(LINE_LIKHO.copy())(new BasicString("Assalam-o-Alikum Dunya!"));
var elements = new BasicArray([new BasicString("sp"), new BasicString("l")]);
for (var x = new BasicNumber(0); (forcond(new BasicNumber(0), (LAMBAI.copy())(elements.copy()), (x).copy())).is_true(); x = (x.copy().added_to(new BasicNumber(1)))){	
	elements.value[x.copy().value] = (oopify.copy())((elements.copy().dived_by(x.copy())));
	
};
for (var i = new BasicNumber(0); (forcond(new BasicNumber(0), new BasicNumber(5), (i).copy())).is_true(); i = (i.copy().added_to(new BasicNumber(1)))){	
	(LINE_LIKHO.copy())((JODH.copy())(new BasicString(", "), elements.copy()));
	
};