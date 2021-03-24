let x = (x => (x => x * 9)(x) + 3)(5)
console.log('=-------------->', x)

let y = y => (y => y * 9)(y) + 3

console.log(y(5))