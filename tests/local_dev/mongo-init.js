let error = true

let res = [
  db.init.drop(),
  db.init.insert({ hello: "world" }),
]

printjson(res)
