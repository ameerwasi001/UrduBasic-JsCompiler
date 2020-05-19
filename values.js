const prompt = require('prompt-sync')()

class RTError extends Error{
  constructor(message) {
    super(message)
    this.name = this.constructor.name
    if (typeof Error.captureStackTrace === 'function') {
      Error.captureStackTrace(this, this.constructor);
    } else {
      this.stack = (new Error(message)).stack;
    }
  }
}

class Value {

    added_to(other){
        return this.illegal_operation(other)
      }

    subbed_by(other){
        return this.illegal_operation(other)
      }

    multed_by(other){
        return this.illegal_operation(other)
      }

    dived_by(other){
        return this.illegal_operation(other)
      }

    moded_by(other){
        return this.illegal_operation(other)
      }

    powed_by(other){
        return this.illegal_operation(other)
      }

    get_comparison_eq(other){
        return this.illegal_operation(other)
      }

    get_comparison_ne(other){
        return this.illegal_operation(other)
      }

    get_comparison_lt(other){
        return this.illegal_operation(other)
      }

    get_comparison_gt(other){
        return this.illegal_operation(other)
      }

    get_comparison_lte(other){
        return this.illegal_operation(other)
      }

    get_comparison_gte(other){
        return this.illegal_operation(other)
      }

    ored_by(other){
        return this.illegal_operation(other)
      }

    anded_by(other){
        return this.illegal_operation(other)
      }

    notted(){
        return this.illegal_operation()
      }

    execute(args){
        return RTResult().failure(this.illegal_operation())
      }

    is_true(){
        return false
      }

    copy(){
        throw new RTError('No copy method defined')
      }

    illegal_operation(other=None){
        if (!other){other = this}
        throw new RTError(
            'Illegal Operation'
        )
    }
}

class BasicNumber extends Value {

    constructor(value){
        super()
        this.value = value
      }

    added_to(other){
        if (other.constructor.name == "BasicNumber"){
            return new BasicNumber(this.value + other.value)
        } else if (other.constructor.name == "BasicString"){
            return other.added_to(String(this))
        } else if (other.constructor.name == "BasicArray"){
            return other.added_to(this)
        } else {
            return this.illegal_operation(other)
          }
        }

    subbed_by(other){
        if (other.constructor.name == "BasicNumber"){
            return new BasicNumber(this.value - other.value)
        } else {
            return null, this.illegal_operation(other)
          }
      }

    multed_by(other){
        if (other.constructor.name == "BasicNumber"){
            let number = new BasicNumber(this.value * other.value)
            return isNaN(number.value)? new BasicNumber(0) : number
        } else if ((other.constructor.name == "BasicString") || (other.constructor.name == "BasicArray")){
            return other.multed_by(this)
        } else {
            return null, this.illegal_operation(other)
          }
      }

    dived_by(other){
        if (other.constructor.name == "BasicNumber"){
            if (other.value == 0){
                throw new RTError(
                "Zero se division"
                )
              }
            return new BasicNumber(this.value / other.value)
        } else {
            return null, this.illegal_operation(other)
          }
        }

    moded_by(other){
        if (other.constructor.name == "BasicNumber"){
            if (other.value == 0) {
                throw new RTError(
                    "Zero se division"
                    )
                }
            return new BasicNumber(this.value % other.value)
        } else {
            return null, this.illegal_operation(other)
          }
        }

    powed_by(other){
        if (other.constructor.name == "BasicNumber"){
            return new BasicNumber(this.value ^ other.value)
          } else {
            return null, this.illegal_operation(other)
          }
        }

    get_comparison_eq(other){
        if (other.constructor.name == "BasicNumber"){
            return new Boolean(this.value == other.value)
          } else {
            return new Boolean(0)
          }
      }

    get_comparison_ne(other){
        if (other.constructor.name == "BasicNumber"){
            return new Boolean(this.value != other.value)
          } else {
            return new Boolean(1)
          }
      }

    get_comparison_lt(other){
        if (other.constructor.name == "BasicNumber"){
            return new Boolean(this.value < other.value)
        } else {
            return null, this.illegal_operation(other)
          }
    }

    get_comparison_gt(other){
        if (other.constructor.name == "BasicNumber"){
            return new Boolean(this.value > other.value)
        } else {
            return null, this.illegal_operation(other)
          }
      }

    get_comparison_lte(other){
        if (other.constructor.name == "BasicNumber"){
            return new Boolean(this.value <= other.value)
        } else {
            return null, this.illegal_operation(other)
          }
      }

    get_comparison_gte(other){
        if (other.constructor.name == "BasicNumber"){
            return new Boolean(this.value >= other.value)
        } else {
            return null, this.illegal_operation(other)
          }
      }

    ored_by(other){
        if (other.constructor.name == "BasicNumber"){
            return new Boolean(this.value || other.value)
        } else {
            return null, this.illegal_operation(other)
          }
      }

    anded_by(other){
        if (other.constructor.name == "BasicNumber"){
            return Boolean(this.value && other.value)
        } else {
            return None, Value.illegal_operation(this, other)
          }
      }

    notted(){
        return new Boolean(this.value == 0 ? 1 : 0)
      }

    is_true(){
        return this.value != 0
      }

    copy(){
        let copy = new BasicNumber(this.value)
        return copy
      }

    toString(){
        return this.value.toString()
      }
}

class BasicInfinity extends BasicNumber{
    constructor(){
        super(Infinity)
      }

    subbed_by(other){
        if (other.constructor.name == "BasicNumber"){
            let number = new BasicNumber(this.value - other.value)
            return isnan(number.value)? new BasicNumber(0) : number
        } else {
            return null, this.illegal_operation(other)
          }
        }

    multed_by(other){
        if (other.constructor.name == "BasicNumber"){
            let number = new BasicNumber(this.value * other.value)
            return isNaN(number.value) ? new BasicNumber(0) : number
        } else if ((other.constructor.name == "BasicString") || (other.constructor.name == "BasicArray")){
            return other.multed_by(this)
        } else {
            return null, this.illegal_operation(other)
          }
    }

    copy(){
        let copy = Infinity()
        return copy
      }

    toString(){
        return "LaMehdood"
      }
}

class BasicString extends Value{
    constructor(value){
        super()
        this.value = value
      }

    added_to(other){
        if (other.constructor.name == "BasicArray"){
            return other.added_to(this)
        } else {
            return new BasicString(this.value + other.value.toString() || other.value.toString())
          }
      }

    multed_by(other){
        if (other.constructor.name == "BasicNumber"){
            return new BasicString(this.value.repeat(other.value))
        } else {
            return null, this.illegal_operation(other)
          }
        }

    dived_by(other){
        if (other.constructor.name == "BasicNumber"){
            let to_return = this.value.split("")[other.value]
            return new BasicString(to_return)
        } else {
            return null, this.illegal_operation(other)
          }
      }

    moded_by(other){
        if (other.constructor.name == "BasicNumber"){
            if (other.value < 0) {
                return new BasicString((this.value.split("")).split(0, other.value).join(""))
            } else {
                return new BasicString((this.value.split("")).split(other.value, 0).join(""))
              }
        } else {
            return null, this.illegal_operation(other)
          }
      }

    get_comparison_eq(other){
        if (other.constructor.name == "BasicString"){
            return new Boolean(this.value == other.value)
        } else {
            return new Boolean(0)
          }
      }

    get_comparison_ne(other){
        if (other.constructor.name == "BasicString"){
            return new Boolean(this.value != other.value)
        } else {
            return new Boolean(1)
          }
      }

    is_true(){
        return len(this.value) > 0
      }

    notted(){
        return new Boolean(!this.is_true())
      }

    ored_by(other){
        if (other.constructor.name == "BasicString"){
            let result = this.is_true() || other.is_true()
            return new Boolean(result)
        } else {
            return null, this.illegal_operation(other)
          }
      }

    anded_by(other){
        if (other.constructor.name == "BasicString"){
            result = this.is_true() && other.is_true()
            return new Boolean(result)
        } else {
            return null, this.illegal_operation(other)
          }
      }

    copy(){
        let copy = new BasicString(this.value)
        return copy
      }

    toString(){
        return `${this.value}`
      }
}

class BasicArray extends Value {
    constructor(elements){
        super()
        this.value = elements
      }

    added_to(other){
        if (other.constructor.name == "BasicArray"){
            return this.multed_by(other)
        } else {
            let new_list = new BasicArray([...this.value])
            new_list.value.push(other)
            return new_list
          }
        }

    subbed_by(other){
      let value = other.value
        if (other.constructor.name == "BasicNumber"){
            let new_list = new BasicArray([...this.value])
            value = value<0 ? (this.value.length + value) : value
            if (value < this.value.length){
                new_list.value.pop(value)
                return new_list
            } else {
                throw new RTError(
                    "Ye index nahi nikal sake kyu ke ye list me mila hi nahi"
                )
              }
        } else {
            return this.illegal_operation(other)
          }
      }

    moded_by(other){
        if (other.constructor.name == "BasicNumber"){
            if (other.value < 0){
                return List(this.value.split(0, other.value))
            } else {
                return List(this.value.split(other.value, 0))
              }
        } else {
            return null, this.illegal_operation(other)
          }
      }

    multed_by(other){
        if (other.constructor.name == "BasicArray"){
            let new_list = new BasicArray([...this.value])
            new_list.value.append(...other.value)
            return new_list, null
        } else {
            return this.added_to(other)
          }
      }

    dived_by(other){
        if (other.constructor.name == "BasicNumber"){
            let value = other.value
            value = value<0 ? (this.value.length + value) : value
            if (value < this.value.length){
                value = value<0 ? (this.value.length + value) : value
                return this.value[value]
            } else {
                throw new RTError(
                    "Ye number ki cheez list me mila hi nahi"
                )
            }
        } else {
            return this.illegal_operation(other)
          }
      }

    truth_of_list(other){
        let truth = []
        if (other.value.length != this.value.length){ return false }
        if (!(other.constructor.name == "BasicArray")){ return false }
        for (let index = 0; index<this.value.length; index++){
            if ((0 <= index) && (index < other.value.length)){
                let call = this.value[index].get_comparison_eq(other.value[index])
                if (call){
                    if (call.state == 1){
                        truth.push(true)
                    } else {
                        break
                      }
                } else {
                    break
                }
              }
            }
        return (truth.length == this.value.length) && (truth.length == other.value.length)
      }

    get_comparison_eq(other){
        if (other.constructor.name == "BasicArray"){
            return new Boolean(this.truth_of_list(other))
        } else {
            return new Boolean(0)
        }
    }

    get_comparison_ne(other){
        if (other.constructor.name == "BasicArray"){
            return new Boolean(!this.truth_of_list(other)), None
        } else {
            return new Boolean(1)
          }
    }

    is_true(){
        return this.value.length>0
    }

    notted(){
        return new Boolean(!this.is_true())
      }

    ored_by(other){
        if (other.constructor.name == "BasicArray"){
            let result = this.is_true() || other.is_true()
            return new Boolean(result)
        } else {
            return null, this.illegal_operation(other)
          }
    }

    anded_by(other){
        if (other.constructor.name == "BasicArray"){
            let result = this.is_true() && other.is_true()
            return new Boolean(result)
        } else {
            return null, this.illegal_operation(other)
          }
    }

    copy(){
        let copy = new BasicArray(this.value)
        return copy
      }

    toString(){
        return `[${this.value.map((x) => x.toString()).join(", ")}]`
      }
}

class Boolean extends BasicNumber {
    constructor(value){
        super(value)
        this.value = value
      }

     toString(){
        return this.state ? 'sahi' : 'galat'
      }

    copy(){
        let copy = new Boolean(this.value)
        return copy
    }
}

class NullObject extends BasicNumber{
    constructor(){
        super(0)
      }

    toString(){
        return 'khali'
      }

    copy(){
        let copy = new NullObject()
        return copy
      }
}

Function.prototype.copy = function () {
    return this
}

function LINE_LIKHO(line){
  console.log(line.toString())
}

function LAMBAI(thing){
  if (!(thing.constructor.name == "BasicArray" || thing.constructor.name == "BasicString")){
    throw new RTError(`${thing} is neither a list or an array`)
  }
  return new BasicNumber(thing.value.length)
}

function JODH(sep, list){
  if (!(sep.constructor.name == "BasicString")){
    throw new RTError(`${sep} is not a string`)
  }
  if (!(list.constructor.name == "BasicArray")){
    throw new RTError(`${list} is not an array`)
  }
  return new BasicString(list.value.join(sep.value))
}

function LIKHO_WAPIS(thing){
  LINE_LIKHO(thing)
  return thing
}

function KYA_NUM(thing){
  return new Boolean(thing.constructor.name == "BasicNumber")
}

function KYA_STR(thing){
  return new Boolean(thing.constructor.name == "BasicString")
}

function KYA_LIST(thing){
  return new Boolean(thing.constructor.name == "BasicArray")
}

function DALO(list, thing){
  if (!(list.constructor.name == "BasicArray")){
    throw new RTError(`${list} is not am array`)
  }
  list.value.append(thing)
}

function MILAO(list1, list2){
  if (!(list1.constructor.name == "BasicArray")){
    throw new RTError(`${list} is not am array`)
  }
  if (!(list2.constructor.name == "BasicArray")){
    throw new RTError(`${list} is not am array`)
  }
  list.value.append(...list2)
}

function MATH_SQRT(num){
  return new BasicNumber(sqrt(num.value))
}

function NIKAL(list, index){
  if (!(list.constructor.name == "BasicArray")){
    throw new RTError(`${list} is not am array`)
  }
  list.value.pop(index.value)
  return new Boolean(thing.constructor.name == "BasicArray")
}

function PUCHO(question){
  return new BasicString(prompt(question.toString()))
}

function forcond(start_value, end_value, step){
  if (((start_value.copy()).get_comparison_lt(end_value.copy())).is_true()) {
    return ((step.copy()).get_comparison_lt(end_value.copy()))
  } else {
    return ((step.copy()).get_comparison_gt(end_value.copy()))
  }
}

var sahi = new Boolean(1)
var galat = new Boolean(0)
var khali = new NullObject()


module.exports = {sahi, galat, khali, forcond,
  PUCHO, MATH_SQRT, LINE_LIKHO,
  MILAO, DALO, NIKAL, KYA_NUM,
  KYA_STR, KYA_LIST, LIKHO_WAPIS,
  JODH, LAMBAI, Value,
  RTError, Boolean, BasicInfinity,
  BasicString, BasicNumber, BasicArray,
  NullObject
}
