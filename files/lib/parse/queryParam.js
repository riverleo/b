import _ from 'lodash';

export default raw => ({
  b: _.toNumber(_.get(raw, 'b')) || undefined, //                             blur   : Number (0...1)
  c: _.get(raw, 'c') ? _.toString(_.get(raw, 'c')) === 'true' : undefined, // crop   : Bool
  h: _.toNumber(_.get(raw, 'h')) || undefined, //                             height : Number
  q: _.toNumber(_.get(raw, 'q')) || undefined, //                             quality: Number (0...1)
  w: _.toNumber(_.get(raw, 'w')) || undefined, //                             width  : Number
});
