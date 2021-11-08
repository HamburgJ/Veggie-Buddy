var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var ItemSchema = new Schema(
  {
    item: {type: String, required: true},
    category: {type: String, required: true},
    name: {type: String, required: true},
    price: {type: String, required: true},
    store: {type: String, required: true},
    image: {type: String, required: true},
    story: {type: String, required: true},
    vegan: {type: Boolean, required: true},
    foods: [{type: String, required: true}],
    location: {type: String, required: true}
  }
);

//Export model
module.exports = mongoose.model('Item', ItemSchema);