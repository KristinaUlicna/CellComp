from lineage import *

t = LineageTree.from_xml("/Users/kristinaulicna/Documents/Rotation_2/tracks_type1.xml")
trees = t.create()      # it's a list of Nodes (=classes)




import json

json_data = json.dumps({
  "result":[
    {
      "run":[
        {
          "action":"stop"
        },
        {
          "action":"start"
        },
        {
          "action":"start"
        }
      ],
      "find": "true"
    }
  ]
})

item_dict = json.loads(json_data)
print len(item_dict['result'][0]['run'])