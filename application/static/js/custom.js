//states n city in india


var citiesByState = {
    Odisha: ["Bhubaneswar","Puri","Cuttack"],
    Maharashtra: ["Mumbai","Pune","Nagpur","boisar"],
    Kerala: ["kochi","Kanpur",'lucknow']
    }

function makeSubmenu(value) {
    if(value.length==0) document.getElementById("citySelect").innerHTML = "<option></option>";
    else {
    var citiesOptions = "";
    for(cityId in citiesByState[value]) {
    citiesOptions+="<option>"+citiesByState[value][cityId]+"</option>";
    }
    document.getElementById("citySelect").innerHTML = citiesOptions;
    }
}