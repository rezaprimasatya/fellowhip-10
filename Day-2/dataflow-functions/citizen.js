function transform(line){
    var values = line.split(',');
    var obj = new Object();
    obj.fullname = values[0];
    obj.phone = values[1];
    obj.hobbies = values[2];
    obj.games = values[3];
    obj.birthdate = values[4];
    var jsonString = JSON.stringify(obj);
    return jsonString;
}